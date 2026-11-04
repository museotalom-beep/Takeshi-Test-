import asyncio,json
from playwright.async_api import async_playwright
BASE='http://127.0.0.1:3000'
REASON='Families need a clear description of child suitability and transport. CRM-01 supports evening email, while WEB-01 shows why a clear mobile booking journey is important.'
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  page=await b.new_page(viewport={'width':1440,'height':1000})
  errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
  await page.goto(BASE,wait_until='domcontentloaded')
  await page.locator('.hero .btn').click()
  async def choose(path,v):
   await page.locator(f'[data-field="{path}"]').select_option(v)
  async def explain(path):
   await page.locator(f'[data-field="{path}"]').fill(REASON)
  async def art(path,id='camp'):
   await page.locator(f'[data-pick="{path}"][data-value="{id}"]').click()
  async def complete():
   await page.locator('[data-action="complete"]').click()
   assert await page.locator('.validation').count()==0,await page.locator('.validation').inner_text() if await page.locator('.validation').count() else ''
  # Real UI input for missions 1-4.
  await art('market.audience','family')
  for k,v in {'goal':'40','evidence':'CRM-01','journey':'consideration'}.items():await choose('market.'+k,v)
  await explain('market.reason');await complete()
  for k,v in {'headline':'family','cta':'family','layout':'responsive','proof':'verified','keyword':'family','destination':'matched'}.items():await choose('web.'+k,v)
  await page.locator('[data-art-path="web.image"][data-art-id="family"]').drag_to(page.locator('[data-art-drop="web.image"]'))
  await art('web.palette','terracotta')
  await page.locator('[data-copy="web.customHeadline"]').fill('A family evening beyond the ordinary')
  await page.locator('[data-copy="web.customHeadline"]').blur()
  assert await page.locator('.site-copy h2').inner_text()=='A family evening beyond the ordinary'
  await explain('web.reason')
  await page.screenshot(path='/tmp/arena-website.png',full_page=True)
  await complete()
  for i in range(2):
   await page.locator(f'[data-creative="{i}"]').click()
   for k,v in {'purpose':'discover' if i==0 else 'followup','subject':'family','preview':'benefit','heading':'family','body':'family','cta':'family','time':'family','evidence':'CRM-01'}.items():await choose(f'email.{i}.'+k,v)
   await art(f'email.{i}.image','family')
   if i:await explain('email.1.reason')
  await page.screenshot(path='/tmp/arena-email.png',full_page=True)
  await complete()
  for i in range(2):
   await page.locator(f'[data-creative="{i}"]').click()
   for k,v in {'format':'carousel' if i==0 else 'story','purpose':'inspire' if i==0 else 'convert','caption':'family','hashtags':'relevant','cta':'family'}.items():await choose(f'social.{i}.'+k,v)
   await art(f'social.{i}.image','family')
   if i:
    await choose('social.1.response','helpful');await explain('social.1.reason')
  await complete()
  # Create all calendar cards through the UI, and exercise drag/drop movement.
  for i in range(12):
   week=i%8+1
   await page.locator(f'[data-add-week="{week}"]').click()
   for k,v in {'audience':'family','channel':'email' if i%2==0 else 'instagram','purpose':'awareness' if week<3 else 'consideration' if week<6 else 'conversion','time':'family','evidence':'CRM-01'}.items():await choose(f'plan.slots.{i}.'+k,v)
  await page.locator('[data-drag-slot="0"] .calendar-card-top').drag_to(page.locator('[data-drop-week="2"] .week-title'))
  assert await page.locator('[data-drop-week="2"] [data-drag-slot="0"]').count()==1
  await choose('plan.slots.0.week','1')
  await choose('plan.response','update');await explain('plan.reason')
  await page.screenshot(path='/tmp/arena-calendar.png',full_page=True)
  await complete()
  for k,v in {'bottleneck':'mobile','test':'moredata','revision':'cta','metric':'bookings','evidence':'WEB-01'}.items():await choose('board.'+k,v)
  await explain('board.reason');await complete()
  await page.locator('[data-action="simulate"]').click()
  assert await page.locator('.journey-stop').count()==4
  await page.screenshot(path='/tmp/arena-simulation.png')
  await page.locator('.modal [data-action="close"]').first.click()
  # Early submission must be blocked.
  await page.locator('[data-action="submit"]').click()
  assert await page.locator('.validation').count()==1
  print('Real UI: all six missions, drag/drop, custom copy, simulation and early-submit guard passed.')
  # Test fixture advances only the stored timer; avoids waiting 40 minutes in automated testing.
  await page.evaluate("""()=>{const s=JSON.parse(localStorage.getItem('campaign-arena-v1'));s.activeSeconds=2400;localStorage.setItem('campaign-arena-v1',JSON.stringify(s));}""")
  await page.reload(wait_until='domcontentloaded')
  await page.locator('[data-action="submit"]').click()
  assert '100' in await page.locator('.final-score').inner_text()
  assert 'CHALLENGE COMPLETE' in await page.locator('.final-status').inner_text()
  async with page.expect_download() as dl:
   await page.locator('.final-banner [data-action="export"]').click()
  downloaded=await dl.value
  await downloaded.save_as('/tmp/arena-export.json')
  report=json.load(open('/tmp/arena-export.json'));assert report['score']==100 and len(report['work']['plan']['slots'])==12
  await page.screenshot(path='/tmp/arena-success.png',full_page=True)
  print('100% final submission and campaign export verified (timer advanced only in test fixture).')
  # Deliberately weaken a full campaign and verify restart flow.
  await page.evaluate("""()=>{const s=JSON.parse(localStorage.getItem('campaign-arena-v1'));s.result=null;s.data.web.layout='desktop';s.data.web.destination='different';s.data.web.proof='invented';s.data.email.forEach(e=>e.purpose='blast');s.data.social[1].response='false';s.data.board.revision='followers';localStorage.setItem('campaign-arena-v1',JSON.stringify(s));}""")
  await page.reload(wait_until='domcontentloaded');await page.locator('[data-action="submit"]').click()
  assert 'RESTART REQUIRED' in await page.locator('.final-status').inner_text()
  await page.locator('[data-action="restart"]').click();await page.locator('[data-action="confirm-restart"]').click()
  s=await page.evaluate("JSON.parse(localStorage.getItem('campaign-arena-v1'))")
  assert s['attempt']==2 and not s['complete'] and not s['data']['plan']['slots'] and s['activeSeconds']<3
  print('Below-80% diagnostic and full restart verified.')
  # Responsive check on real populated pages.
  for width in [390,768,1024,1440]:
   await page.set_viewport_size({'width':width,'height':900})
   assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth'),width
  assert not errs,errs
  print('No JavaScript errors; no horizontal overflow at 390, 768, 1024, 1440px.')
  await b.close()
asyncio.run(main())
