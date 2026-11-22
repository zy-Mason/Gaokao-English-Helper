# Copyright (C) 2026 Mason 朱懿
from tools.word_jsoner import aijsoner
import asyncio
tsxt = '''
▶ grassy adj 长满草的
▶ grassland n [U] & [C] 草原；草地
▶ grass roots n [复数] 草根阶层；平民百姓
grateful /ˈɡreɪtfl/ adj 感激的 反 ungrateful
be extremely grateful to sb for sth 因某事非常感激某人
give sb a grateful look / smile 感激地看某人一眼 / 给某人一个感激的微笑
▶ gratefully adv 感激地
▶ gratitude n [U] 感激之情；感谢
express one's gratitude to sb for sth 为某事对某人表示感谢
gravity /ˈɡrævəti/ n [U]
① 重力；引力
② [正式] 严重性；严肃
realise the gravity of the situation 意识到形势的严重性
speak with great gravity 说话时十分严肃
▶ zero gravity n [U] 零重力状态；失重状态
great /ɡreɪt/
adj ① [非正式] 极好的；很棒的
② (体积、数量、程度等) 大的；伟大的；重大的
adv [非正式] 极好地；很棒地
n [C] [非正式] 伟人；杰出事物
an album of jazz greats 爵士名曲集
▶ greatly adv [正式] 极大地；非常
Your help would be greatly appreciated. 如蒙帮助，感激不尽。
▶ greatness n [U] 伟大；杰出
greedy /ˈɡriːdi/ adj 贪婪的；贪吃的
stare at sth with greedy eyes 用贪婪的目光盯着某物
be greedy for sth 极度渴望某事物
▶ greedily adv 贪婪地
▶ greed n [U] 贪婪；贪吃
green /ɡriːn/
adj 绿色的；青的；不成熟的
a green salad / tomato / hand 蔬菜沙拉 / 没熟的西红柿 / 生手
adopt a greener lifestyle 采取更环保的生活方式
be green with envy 非常嫉妒；眼红
have green fingers / a green thumb 擅长园艺
n [U] & [C] 绿色；[复数] 绿叶蔬菜
vt 绿化；使重视环境问题

ground
greenhouse /ˈɡriːnhaʊs/ n [C] 温室
▶ greenhouse gas n [C] 温室气体（尤指二氧化碳）
greet /ɡriːt/ vt 打招呼；迎接
be greeted by a grand view / problems 壮丽景色映入眼帘 / 问题接踵而来
▶ greeting n [U] & [C] 问候；[复数] 祝词
a greeting(s) card 贺卡
exchange greetings 互相问候
grey / gray /ɡreɪ/
adj 灰（白）的；灰暗的；沉闷的
a grey-haired old lady 头发灰白的老太太
a grey day / future 阴沉沉的一天 / 暗淡的未来
grey area 灰色地带（指难以界定和处理的情况）
n [C] & [U] 灰色
vi （头发）变花白
a full head of greying hair 满头华发
grocery /ˈɡrəʊsəri; ˈɡroʊsəri/
n [C] 食品杂货店；[复数] 食品杂货
▶ grocer n [C] 食品杂货商
ground /ɡraʊnd/
n ① [U] 地（面）；[C] 场地
a sports / parking ground 运动场 / 停车场
② [U] 立场；（知识等的）领域
have common ground 有共同的观点
③ [C] [复数] 根据；理由
do sth on environmental grounds 出于环保的原因做某事
gain / lose ground 获得进展 / 让步；失利
get (sth) off the ground （使某事）顺利开始
have / keep one's feet on the ground 脚踏实地
hold / stand one's ground 坚持自己的主张
break new ground 有新突破
▶ groundbreaking adj 开创性的；创新的
vt & vi （使）（船）搁浅；使停飞；vt 罚（小孩）禁足
Both boats grounded on a mud bank. 两只船都在泥滩上搁浅了。
The balloon was grounded by strong winds. 热气球因强风停飞。
ground sb for a week 罚某人一周不准出门
be grounded in / on sth 以某事物为根据
▶ ground floor n [C] 底层；一楼 (AmE first floor)
▶ groundwater n [U] 地下水
▶ ground rule n [复数] 基本原则'''

def test_jsoner():
    async def main():
        result = await aijsoner(tsxt)
        print(result)
    asyncio.run(main())

jsonexample={"items":[{"en":"grassy","zh":"长满草的"},{"en":"grassland","zh":"草原；草地"},{"en":"grass roots","zh":"草根阶层；平民百姓"},{"en":"grateful","zh":"感激的"},{"en":"be extremely grateful to sb for sth","zh":"因某事非常感激某人"},{"en":"give sb a grateful look","zh":"感激地看某人一眼"},{"en":"give sb a grateful smile","zh":"给某人一个感激的微笑"},{"en":"gratefully","zh":"感激地"},{"en":"gratitude","zh":"感激之情；感谢"},{"en":"express one's gratitude to sb for sth","zh":"为某事对某人表示感谢"},{"en":"gravity","zh":"重力；引力"},{"en":"gravity","zh":"严重性；严肃"},{"en":"realise the gravity of the situation","zh":"意识到形势的严重性"},{"en":"speak with great gravity","zh":"说话时十分严肃"},{"en":"zero gravity","zh":"零重力状态；失重状态"},{"en":"great","zh":"极好的；很棒的"},{"en":"great","zh":"大的；伟大的；重大的"},{"en":"great","zh":"极好地；很棒地"},{"en":"great","zh":"伟人；杰出事物"},{"en":"an album of jazz greats","zh":"爵士名曲集"},{"en":"greatly","zh":"极大地；非常"},{"en":"Your help","zh":"如蒙帮助"},{"en":"would be greatly appreciated","zh":"感激不尽"},{"en":"greatness","zh":"伟大；杰出"},{"en":"greedy","zh":"贪婪的；贪吃的"},{"en":"stare at sth with greedy eyes","zh":"用贪婪的目光盯着某物"},{"en":"be greedy for sth","zh":"极度渴望某事物"},{"en":"greedily","zh":"贪婪地"},{"en":"greed","zh":"贪婪；贪吃"},{"en":"green","zh":"绿色的；青的；不成熟的"},{"en":"a green salad","zh":"蔬菜沙拉"},{"en":"a green tomato","zh":"没熟的西红柿"},{"en":"a green hand","zh":"生手"},{"en":"adopt a greener lifestyle","zh":"采取更环保的生活方式"},{"en":"be green with envy","zh":"非常嫉妒；眼红"},{"en":"have green fingers","zh":"擅长园艺"},{"en":"have a green thumb","zh":"擅长园艺"},{"en":"green","zh":"绿色；绿叶蔬菜"},{"en":"green","zh":"绿化；使重视环境问题"},{"en":"greenhouse","zh":"温室"},{"en":"greenhouse gas","zh":"温室气体（尤指二氧化碳）"},{"en":"greet","zh":"打招呼；迎接"},{"en":"be greeted by a grand view","zh":"壮丽景色映入眼帘"},{"en":"be greeted by problems","zh":"问题接踵而来"},{"en":"greeting","zh":"问候；祝词"},{"en":"a greeting(s) card","zh":"贺卡"},{"en":"exchange greetings","zh":"互相问候"},{"en":"grey / gray","zh":"灰（白）的；灰暗的；沉闷的"},{"en":"a grey-haired old lady","zh":"头发灰白的老太太"},{"en":"a grey day","zh":"阴沉沉的一天"},{"en":"a grey future","zh":"暗淡的未来"},{"en":"grey area","zh":"灰色地带（指难以界定和处理的情况）"},{"en":"grey / gray","zh":"灰色"},{"en":"grey / gray","zh":"（头发）变花白"},{"en":"a full head of greying hair","zh":"满头华发"},{"en":"grocery","zh":"食品杂货店；食品杂货"},{"en":"grocer","zh":"食品杂货商"},{"en":"ground","zh":"地（面）"},{"en":"ground","zh":"场地"},{"en":"a sports ground","zh":"运动场"},{"en":"a parking ground","zh":"停车场"},{"en":"ground","zh":"立场"},{"en":"ground","zh":"（知识等的）领域"},{"en":"have common ground","zh":"有共同的观点"},{"en":"ground","zh":"根据；理由"},{"en":"do sth on environmental grounds","zh":"出于环保的原因做某事"},{"en":"gain ground","zh":"获得进展"},{"en":"lose ground","zh":"让步；失利"},{"en":"get (sth) off the ground","zh":"（使某事）顺利开始"},{"en":"have one's feet on the ground","zh":"脚踏实地"},{"en":"keep one's feet on the ground","zh":"脚踏实地"},{"en":"hold one's ground","zh":"坚持自己的主张"},{"en":"stand one's ground","zh":"坚持自己的主张"},{"en":"break new ground","zh":"有新突破"},{"en":"groundbreaking","zh":"开创性的；创新的"},{"en":"ground","zh":"（使）（船）搁浅"},{"en":"ground","zh":"使停飞"},{"en":"ground","zh":"罚（小孩）禁足"},{"en":"Both boats","zh":"两只船"},{"en":"grounded on a mud bank","zh":"都在泥滩上搁浅了"},{"en":"The balloon","zh":"热气球"},{"en":"was grounded by strong winds","zh":"因强风停飞"},{"en":"ground sb for a week","zh":"罚某人一周不准出门"},{"en":"be grounded in sth","zh":"以某事物为根据"},{"en":"be grounded on sth","zh":"以某事物为根据"},{"en":"ground floor","zh":"底层；一楼"},{"en":"groundwater","zh":"地下水"},{"en":"ground rule","zh":"基本原则"}]}



