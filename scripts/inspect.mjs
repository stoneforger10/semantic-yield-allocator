import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import crypto from 'node:crypto';
const [address,creator,name,expected] = process.argv.slice(2);
const ascii=x=>JSON.stringify(x).replace(/[\u007f-\uffff]/g,c=>'\\u'+c.charCodeAt(0).toString(16).padStart(4,'0'));
const canonical=x=>x===null||typeof x!=='object'?ascii(x):Array.isArray(x)?'['+x.map(canonical).join(',')+']':
  '{'+Object.keys(x).sort().map(k=>ascii(k)+':'+canonical(x[k])).join(',')+'}';
const hash=x=>crypto.createHash('sha256').update(canonical(x)).digest('hex');
function checkRoot(x){const {root,...body}=x;if(hash(body)!==root)throw Error('Root mismatch');}
const client=createClient({chain:studionet});
async function read(functionName,args){
  try{return await client.readContract({address,functionName,args});}
  catch{throw Error('Sanitized contract read failure: '+functionName);}
}
function choose(stats,inventory){
  const available=stats.map((s,i)=>i).filter(i=>stats[i].attempts<inventory[i].items.length);
  for(const i of available)if(stats[i].attempts===0)return i;
  return available.reduce((best,i)=>{
    const score=j=>Math.floor((stats[j].hits+1)*10000/(stats[j].known+2))+Math.floor(10000/(stats[j].attempts+1));
    return best<0||score(i)>score(best)?i:best;
  },-1);
}
try{
  const key=await read('experiment_key',[creator,name]);
  const job=await read('get_experiment',[key]);
  if(job.spec.key!==key||job.spec.name!==name||hash(job.spec)!==job.spec_root)throw Error('Spec binding');
  if(expected&&job.state!==expected)throw Error('Unexpected state: '+job.state);
  let previous=job.activation.root;
  if(previous)checkRoot(job.activation);
  let stats=job.inventory.map(()=>({attempts:0,known:0,hits:0}));
  const reports=[];
  for(let trial=0;trial<job.trials;trial++){
    const r=await read('get_observation',[key,trial]);checkRoot(r);
    const b=r.binding,i=choose(stats,job.inventory);
    if(b.experiment!==key||b.trial!==trial||b.spec_root!==job.spec_root||b.prior_root!==previous
        ||canonical(b.stats)!==canonical(stats)||b.arm!==i||b.cursor!==stats[i].attempts
        ||canonical(b.item)!==canonical(job.inventory[i].items[stats[i].attempts]))throw Error('Selection binding');
    if(r.source.status==='OK'){
      if(r.source.http!==200||r.source.hash!==job.spec.sha256||hash(r.text)!==b.item.text_hash)throw Error('Source binding');
    }else if(r.label!=='UNKNOWN'||r.text!=='')throw Error('Unacquired reward');
    stats[i].attempts++;
    if(r.label!=='UNKNOWN'){stats[i].known++;if(r.label==='HIT')stats[i].hits++;}
    if(canonical(stats)!==canonical(r.after.stats)||r.after.trials!==trial+1)throw Error('Statistics binding');
    previous=r.root;
    reports.push({trial,arm:job.inventory[i].id,item:b.item.id,label:r.label,root:r.root,source:r.source});
  }
  if(previous&&previous!==job.last_root)throw Error('Chain head');
  if(canonical(stats)!==canonical(job.stats))throw Error('Final statistics');
  const next=job.state==='ACTIVE'?await read('next_trial',[key]):null;
  console.log(JSON.stringify({key,state:job.state,trials:job.trials,stats:job.stats,next,reports,roots_verified:true}));
}catch(error){console.error(error.message);process.exitCode=1;}
