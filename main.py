import time
import random
import requests
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

exe = Service(executable_path='driver/chromedriver.exe')
options = webdriver.ChromeOptions()
ua = UserAgent()
user_agent = ua.random
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--start-maximized")
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(service=exe, options=options)
actions = ActionChains(driver)
head = {
    'authority': 'pokepower.ru',
    'method': 'POST',
    'path': '/do/route',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-length': '24',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://pokepower.ru',
    'referer': 'https://pokepower.ru/world',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': user_agent,
    'x-requested-with': 'XMLHttpRequest'
}
cookies = {}
route = {'id': 'route', 'type': 'go', 'val': 0}
npc = {'id': 'npc', 'type': 'addons', 'val[]': 'heal'}
gendr = {'бесполый': 'fas fa-genderless', 'мужской': 'fas fa-mars', 'женский': 'женский'}
pokebols = {
    'покебол': '3',
    'гритбол': '4',
    'мастербол': '5',
    'ультрабол': '6',
    'генобол': '109',
    'шайнибол': '123',
    'дистанцбол': '316',
    'сафарибол': '318',
    'взломанный шайнибол': '392'
}
maps = {
    'тропа_13': 341,
    'деревня_тапу': 342,
    'засушливая_равнина': 357,
    'песчаные_дюны': 499,
    'тропа_6': 361,
    'пляж_хано': 360,
    'хихи': 370,
    'церулин': 31,
    'дорога_9': 35,
}
suma = {'монета': '0'}
name = ''
pas = ''
gendcat = ''
valu = '0'
xth = "//img[@src='/img/world/items/small/{}.png']"
xtpb = ''
x = 0
y = 0
z = 1
heal = []
healing = []

try:
    wdval = input('Количество проводимых боёв(Не обязательно указывать): ')
    if not wdval:
        wdval = random.randint(500, 1300)
        print('Случайным образом выбрано количество боёв - ', wdval)
    path = input('Введите путь до Покецентра(прим. дорога_1-паллет): ').lower().split('-')
    if not path:
        print('Лечение отключено.')
    else:
        print('Маршрут до Покецентра составлен...')
        if len(path) >= 1:
            for r in path:
                heal.append(maps[r])
            healing.extend(heal)
            heal.reverse()
            healing.extend(heal)
            healing.insert(len(path), 32)
        else:
            healing.append(maps[path])
            healing.extend(healing)
            healing.insert(1, 32)
    item = input('Предмет/ы из покемона(оставьте пустым, если не нужно): ')
    if not item:
        print('Функция дропа предмета - отключена.')
    else:
        valu = input('Количество желаемого предмета: ')
        if not valu:
            valu = '1'
        else:
            suma[item.lower()] = '0'
    catch = input('Укажите "#XXX Имя покемона", для его ловли(оставьте пустым, если не нужно): ')
    if not catch:
        print('Функция ловли покемонов - отключена.')
    else:
        gendcat = input('Гендер ловимого покемона(Мужской/Женский/Бесполый/Ничего - для ловли всех): ').lower()
        if not gendcat:
            print('Покемоны всех гендеров будут пойманны.')
        else:
            if gendcat in gendr:
                gendcat = gendr[gendcat]
        pbl = input('Выберите Бол для ловли(Покебол - по умолчанию): ').lower()
        if not pbl:
            pbl = '3'
            xtpb = xth.format(pbl)
        else:
            if pbl in pokebols:
                pbl = pokebols[pbl]
                xtpb = xth.format(pbl)
    print(time.strftime('%H:%M:%S', time.localtime()), '- Запуск программы')
    #driver.minimize_window() сворачивает браузер
    driver.get('https://pokepower.ru')
    driver.find_element(By.CLASS_NAME, 'Auth').click()
    driver.find_element(By.ID, 'authLogin').send_keys(name)
    driver.find_element(By.ID, 'authPassword').send_keys(pas + Keys.ENTER)
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'BtnAuth').click()
    driver_cookies = driver.get_cookies()
    for cookie in driver_cookies:
        cookies[cookie['name']] = cookie['value']
    while True:
        time.sleep(1)
        if driver.find_elements(By.XPATH, "//div[@id='locationPreloader' and @style='display: none;']"):
            break
        else:
            continue
    driver.find_element(By.XPATH, "//div[@class='Button NoActive' and @onclick='PP.fight.setHunt(this);']").click()
    while z <= int(wdval):
        waiting = driver.find_element(By.CLASS_NAME, 'DivMap')
        time.sleep(1)
        if driver.find_elements(By.CLASS_NAME, 'Battle'):
            time.sleep(1)
            namepok = driver.find_element(By.XPATH, "//*[@id='battleMap']/div/div[4]/div[2]/div[2]/div[1]").text
            if driver.find_elements(By.XPATH, "//*[@id='battleMap']/div/div[4]/div[1]/div[@class='pok1-color namePokemon Name __name']"):
                driver.find_element(By.XPATH, "//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[2]/i").click()
                time.sleep(3)
                driver.find_element(By.XPATH, "//img[@src='/img/world/items/small/109.png']").click()
                print(catch, '- шайни был успешно пойман!')
                continue
            if namepok.lower() == catch.lower():
                gender = driver.find_element(By.XPATH, "//*[@id='battleMap']/div/div[4]/div[2]/div[2]/div[2]/i").get_attribute('class')
                if gender == gendcat:
                    driver.find_element(By.XPATH, "//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[2]/i").click()
                    time.sleep(3)
                    if driver.find_element(By.XPATH, xtpb).click():
                        driver.find_element(By.XPATH, "//img[@src='/img/world/items/small/3.png']").click()
                    else:
                        print('Закончились выбранные болы и Покеболы.')
                        break
                    time.sleep(1)
                    if driver.find_elements(By.CLASS_NAME, 'Battle'):
                        y += 1
                        print(y, end='. ')
                        print('Повторная попытка поимки', namepok)
                        continue
                    else:
                        z += 1
                        y = 0
                        print(namepok, 'успешно пойман с выбранным гендером!')
                        continue
                elif not gendcat:
                    driver.find_element(By.XPATH, "//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[2]/i").click()
                    time.sleep(3)
                    if driver.find_element(By.XPATH, xtpb).click():
                        driver.find_element(By.XPATH, "//*img[@src='/img/world/items/small/3.png']").click()
                    else:
                        print('Закончились выбранные болы и Покеболы.')
                    time.sleep(1)
                    if driver.find_elements(By.CLASS_NAME, 'Battle'):
                        y += 1
                        print(y, end='. ')
                        print('Повторная попытка поимки', namepok)
                        continue
                    else:
                        y = 0
                        z += 1
                        print(namepok, 'успешно пойман!')
                        continue
            nopp = len(driver.find_elements(By.XPATH, "//div[@class=' Move']//div[@class='Name MoveCategory1' or @class='Name MoveCategory2']"))
            if nopp <= 0:
                driver.find_element(By.XPATH, "//i[@class='fal fa-flag']").click()
                driver.switch_to.alert.accept()
                driver.find_element(By.XPATH, "//div[@class='Button' and @onclick='PP.fight.setHunt(this);']").click()
                time.sleep(2)
                driver.find_element(By.XPATH, '//*[@id="battleMap"]/div/div[4]/div[3]/div[3]/div[5]').click()
                print('Программа приостановлена, закончились PP', 'Процесс лечения запущен', end='...', sep='\n')
                time.sleep(3)
                loc = driver.find_element(By.XPATH, "//div[@class='NameLoc']").text.lower().replace(' ', '_').replace('№', '')
                healing.append(maps[loc])
                for v in healing:
                    route['val'] = v
                    requests.post('https://pokepower.ru/do/route', headers=head, data=route, cookies=cookies)
                    if v == 32:
                        route['val'] = v
                        requests.post('https://pokepower.ru/do/npc', headers=head, data=npc, cookies=cookies)
                driver.refresh()
                while True:
                    if driver.find_element(By.ID, 'locationPreloader'):
                        if driver.find_element(By.CLASS_NAME, 'BtnAuth'):
                            driver.find_element(By.CLASS_NAME, 'BtnAuth').click()
                            break
                        else:
                            continue
                    else:
                        continue
                print('Ок', 'Программа продолжена.', sep='\n', )
                driver.find_element(By.CLASS_NAME, 'BtnAuth').click()
                time.sleep(1)
                driver.find_element(By.XPATH, "//div[@class='Button NoActive' and @onclick='PP.fight.setHunt(this);']").click()
                continue
            driver.find_element(By.XPATH, "//div[@class=' Move']//div[@class='Name MoveCategory1' or @class='Name MoveCategory2']").click()
            while driver.find_elements(By.XPATH, "//*[@id='battleMap']/div/div[2]/div[2]/center/img"):
                time.sleep(1)
                continue
            if driver.find_elements(By.CLASS_NAME, 'Battle'):
                y += 1
                print(y, end='. ')
                print(namepok, 'ранен, повторная попытка.')
                continue
            else:
                y = 0
                x += 1
                z += 1
                notdrop = driver.find_element(By.XPATH, "//*[@class='noty plus']/div[3]").text
                drrp = notdrop.replace('\n', ' ').lower()
                print(x, end='. ')
                print(namepok, 'побежден!', 'Дроп:', notdrop.replace('\n', ', '))
                drop = drrp.replace('x', '')
                drlt = drop.split(' ', 2)
                suma[drlt[0]] = int(suma[drlt[0]]) + int(drlt[1])
                if len(drlt) > 2:
                    if drlt[2] in suma:
                        suma[drlt[2]] = int(suma[drlt[2]]) + 1
                    elif len(drlt[2]) <= 2:
                        pass
                    else:
                        suma[drlt[2]] = '1'
                if not item:
                    continue
                else:
                    if int(valu) <= int(suma[item.lower()]):
                        print('Выбит указанный предмет:', item, '=', valu)
                        break
                    else:
                        continue
        else:
            actions.move_to_element(waiting).perform()
    else:
        print(time.strftime('%H:%M:%S', time.localtime()), '- Программа завершила работу, закончилось указанное число боёв.')
except Exception as ex:
    print(ex)
finally:
    print(time.strftime('%H:%M:%S', time.localtime()), '- Итого выбито:', suma)
    driver.close()
    driver.quit()