import test from 'node:test';
import assert from 'node:assert/strict';
import {freshState,AUDIENCES,evaluate,requirements,canSubmit,cost,outcome} from '../engine.js';
export function campaign(a='family'){
 const s=freshState();const ev=AUDIENCES[a].evidence;
 const reason='The audience evidence supports this decision because it removes a documented booking barrier and connects the message to a measurable business objective.';
 s.data.market={audience:a,goal:'40',evidence:ev,journey:'consideration',reason};
 s.data.web={image:a==='student'?'adventure':a,headline:a,cta:a,layout:'responsive',proof:'verified',keyword:a,destination:'matched',reason};
 s.data.email=[{purpose:'discover'},{purpose:'followup',reason}].map(e=>({...e,subject:a,heading:a,body:a,cta:a,time:a,evidence:ev,preview:'benefit',image:'camp'}));
 s.data.social=[{purpose:'inspire',format:'carousel'},{purpose:'convert',format:'story',response:'helpful',reason}].map(e=>({...e,image:'camp',caption:a,hashtags:'relevant',cta:a}));
 s.data.plan={slots:Array.from({length:12},(_,i)=>({week:i%8+1,audience:a,channel:i%2?'instagram':'email',purpose:i%8<2?'awareness':i%8<5?'consideration':'conversion',time:a,evidence:ev})),response:'update',reason};
 s.data.board={bottleneck:'mobile',evidence:'WEB-01',test:'moredata',revision:'cta',metric:'bookings',reason};
 s.complete=[0,1,2,3,4,5];s.activeSeconds=2400;return s;
}
for(const a of Object.keys(AUDIENCES))test(`A coherent ${a} campaign can pass every mission and earn 100`,()=>{const s=campaign(a);for(let i=0;i<6;i++)assert.deepEqual(requirements(s,i),[]);assert.equal(evaluate(s).score,100);assert.equal(canSubmit(s),true);});
test('Submission requires 40 active minutes, all saved missions, and complete work',()=>{const s=campaign();s.activeSeconds=2399;assert.equal(canSubmit(s),false);s.activeSeconds=2400;s.complete.pop();assert.equal(canSubmit(s),false);s.complete.push(5);delete s.data.board.reason;assert.equal(canSubmit(s),false);});
test('Budget includes all scheduled channels and blocks overspending',()=>{const s=campaign();s.data.plan.slots.forEach(x=>x.channel='paid');assert.equal(cost(s.data.plan.slots),3360);assert.match(requirements(s,4).join(' '),/within AED/);assert.equal(canSubmit(s),false);});
test('Eight weeks and twelve placements are distinct requirements',()=>{const s=campaign();s.data.plan.slots.forEach(x=>x.week=1);assert.match(requirements(s,4).join(' '),/all eight/);s.data.plan.slots=s.data.plan.slots.slice(0,8);assert.match(requirements(s,4).join(' '),/at least 12/);});
test('Wrong CRM timing evidence reduces strategic score',()=>{const s=campaign();s.data.email.forEach(e=>e.evidence='CRM-03');s.data.plan.slots.forEach(e=>e.time='premium');const r=evaluate(s);assert.equal(r.rows.find(x=>x.area==='Email campaign').score,15);assert.equal(r.rows.find(x=>x.area==='Eight-week coherence').score,15);});
test('A premature A/B winner loses analysis credit',()=>{const s=campaign();s.data.board.test='winner';assert.equal(evaluate(s).rows.at(-1).score,7);});
test('Incoherent marketing cannot pass simply by filling fields',()=>{const s=campaign();s.data.web.layout='desktop';s.data.web.destination='different';s.data.web.proof='invented';s.data.email.forEach(e=>e.purpose='blast');s.data.social[1].response='false';s.data.board.revision='followers';assert.ok(evaluate(s).score<80);});
test('Simulation responds to strategy and preserves device totals',()=>{const s=campaign(),good=outcome(s);s.data.web.layout='desktop';s.data.web.destination='different';s.data.email.forEach(e=>e.purpose='blast');const weak=outcome(s);assert.ok(good.bookings>weak.bookings);assert.equal(good.mobile+good.desktop,good.visits);assert.equal(good.mobileBookings+good.desktopBookings,good.bookings);});
test('Restart clears work and time, while preserving the attempt number',()=>{const s=freshState(2);assert.equal(s.attempt,2);assert.equal(s.activeSeconds,0);assert.deepEqual(s.complete,[]);assert.equal(s.result,null);assert.deepEqual(s.data.plan.slots,[]);});
