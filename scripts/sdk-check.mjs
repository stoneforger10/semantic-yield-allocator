import assert from 'node:assert/strict';
import {abi} from 'genlayer-js';
const {calldata} = abi;
for (const [method,args] of [['activate',['a'.repeat(64)]], ['step',['a'.repeat(64),0]], ['expire',['a'.repeat(64)]]]) {
  const encoded=calldata.encode(calldata.makeCalldataObject(method,args,{}));
  assert.deepEqual(calldata.encode(calldata.decode(encoded)),encoded);
}
console.log('3 SDK calldata roundtrips passed');
