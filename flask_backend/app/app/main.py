from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from .common import security
from datetime import datetime
import sys
import json

app = Flask(__name__)

# Connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

RecipeTag = db.Table("RecipeTag",
    db.Column("recipe_id", db.Integer, db.ForeignKey("RecipeInfo.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("TagInfo.id"), primary_key=True)
)

RecipeConstitution = db.Table("RecipeConstitution",
    db.Column("recipe_id", db.Integer, db.ForeignKey("RecipeInfo.id"), primary_key=True),
    db.Column("constitution_id", db.Integer, db.ForeignKey("ConstitutionInfo.id"), primary_key=True)
)


# Set ORM
class UserInfo(db.Model):
    # / **
    # *UserId: 16
    # *name: 臧艺
    # *phone: 15168212330
    # *height: 173
    # *weight: 22
    # *sex: true
    # *BirthDay: 2017 - 07 - 16
    # T00: 00:00
    # *labourIntensity: 优秀
    # *HeadImage: null
    # *constitution: 气虚质
    # *score: 0
    # *age: 0
    # *Token: null
    # * /
    __tablename__ = 'UserInfo'
    UserId = db.Column(db.Integer, primary_key=True)
    user_account = db.Column(db.String(45), unique=True)
    user_password = db.Column(db.String(100))
    name = db.Column(db.String(45))
    phone = db.Column(db.String(45), unique=True)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    sex = db.Column(db.Boolean)
    BirthDay = db.Column(db.DateTime)
    labourIntensity = db.Column(db.Integer)
    HeadImage = db.Column(db.String(100))
    constitution = db.Column(db.String(1000))
    score = db.Column(db.Integer)
    age = db.Column(db.Integer)
    Token = db.Column(db.String(100))

    def __init__(self, user_account, user_password):
        self.user_account = user_account
        self.user_password = user_password
        self.phone = user_account  # Use the phone number as account
        self.weight = 0
        self.height = 0
        self.sex = True
        self.BirthDay = datetime.isoformat(datetime.today())
        self.labourIntensity = 0
        self.HeadImage = " "
        self.constitution = " "
        self.score = 0
        self.age = 0
        self.Token = security.generate_token(user_account)

    def serialize(self):
        return{
            'UserId': self.UserId,
            'name': self.name,
            'phone': self.phone,
            'height': self.height,
            'weight': self.weight,
            'sex': self.sex,
            'BirthDay': datetime.isoformat(self.BirthDay),
            'labourIntensity': self.labourIntensity,
            'constitution': self.constitution,
            'score': self.score,
            'age': self.age,
            'Token': self.Token,
        }


class CateInfo(db.Model):
    # / **
    # *id: 113
    # *name: 西餐3
    # *titleImage: http: // ......
    # *address: 杭州市拱墅区祥园路 - 道路
    # *phone: 18857120152
    # *category: 5
    # *sales: 111
    # *consumption: 22
    # *discount: 满100减200
    # *distance: 0
    # * /
    __tablename__ = 'CateInfo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    titleImage = db.Column(db.String(500))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(45))
    category = db.Column(db.Integer)
    sales = db.Column(db.String(45))
    consumption = db.Column(db.String(45))
    discount = db.Column(db.String(50))
    distance = db.Column(db.String(45))

    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'titleImage': self.titleImage,
            'address': self.address,
            'phone': self.phone,
            'category': self.category,
            'sales': self.sales,
            'consumption': self.consumption,
            'discount': self.discount,
            'distance': self.distance,
        }


class RecipeInfo(db.Model):
    # / **
    # *id: 1
    # *name: 食谱1
    # *titleImage: http: //......
    # *ConstitutionPercentage: 0
    # *sales: 12
    # *price: 66.00
    # *Tags: ["清蒸", "爆炒"]
    # *Restaurant_Name: 餐厅2
    # *Restaurant_Address: 杭州市拱墅区拱墅区
    # *distance: null
    # *category: 3
    # * /
    __tablename__ = 'RecipeInfo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    titleImage = db.Column(db.String(500))
    ConstitutionPercentage = db.Column(db.String(200))
    sales = db.Column(db.String(45))
    price = db.Column(db.Float(2))
    Restaurant_Name = db.Column(db.String(50))
    Restaurant_Address = db.Column(db.String(100))
    category = db.Column(db.String(10))
    distance = db.Column(db.String(45))
    foodRecipe = db.Column(db.String(500))
    tag = db.Column(db.String(20))
    Tag = db.relationship('TagInfo', secondary=RecipeTag, lazy='subquery',
                           backref=db.backref('Recipes', lazy=True))
    Constitution = db.relationship('ConstitutionInfo', secondary=RecipeConstitution, lazy='subquery',
                                   backref=db.backref('Recipes', lazy=True))
    RestaurantId = db.Column(db.Integer)

    def serialize(self):
        tags = []
        constitutions = []

        for i in self.Tag:
            tags.append(i.name)
        for j in self.Constitution:
            constitutions.append(j.name)

        return{
            'id': self.id,
            'name': self.name,
            'titleImage': self.titleImage,
            'ConstitutionPercentage': self.ConstitutionPercentage,
            'sales': self.sales,
            'price': self.price,
            'Restaurant_Name': self.Restaurant_Name,
            'Restaurant_Address': self.Restaurant_Address,
            'category': self.category,
            'RestaurantID': self.RestaurantId,
            'Tags': tags,
            'tag': self.tag,
            'Constitution': constitutions,
            'foodRecipe': json.loads(self.foodRecipe),
            'images': [self.titleImage],
        }


class ArticleInfo(db.Model):
    __tablename__ = "ArticleInfo"
    ArticleId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(10000))
    TitleImage = db.Column(db.String(200))
    ConstitutionPercentage = db.Column(db.Integer)
    clickCount = db.Column(db.Integer)
    loveCount = db.Column(db.Integer)
    aTime = db.Column(db.DateTime)
    PointPraise = db.Column(db.Boolean)
    tag = db.Column(db.String(20))
    url = db.Column(db.String(100))

    def serialize(self):
        return{
            "ArticleId": self.ArticleId,
            "content": self.content,
            "TitleImage": self.TitleImage,
            "tags": [self.tag],
            "ConstitutionPercentage": self.ConstitutionPercentage,
            "cilckCount": self.clickCount,
            "loveCount": self.loveCount,
            "aTime": datetime.isoformat(self.aTime),
            "PointPraise": self.PointPraise,
            "url": self.url,
            "title": self.title,
        }


# UserCate = db.Table("UserCate",
#     db.Column("user_id", db.Integer, db.ForeignKey("UserInfo.UserId"), primary_key=True),
#     db.Column("cate_id", db.Integer, db.ForeignKey("CateInfo.id"), primary_key=True),
#     db.Column('cusLikeOrNot', db.Boolean)
# )


class FoodInfo(db.Model):
    __tablename__ = "FoodInfo"
    FoodId = db.Column(db.Integer, primary_key=True)
    FoodName = db.Column(db.String(20))
    FoodWeight = db.Column(db.Integer)

    def serialize(self):
        return{
            "FoodId": self.FoodId,
            "FoodName": self.FoodName,
            "FoodWeight": self.FoodWeight,
        }


class UserFood(db.Model):
    __tablename__ = "UserFood"
    user_id = db.Column(db.Integer, db.ForeignKey("UserInfo.UserId"), primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey("FoodInfo.FoodId"), primary_key=True)
    WhetherLike = db.Column(db.Integer)

    def __init(self):
        self.WhetherLike = 0

    def __init__(self, user_id, food_id, WhetherLike):
        self.user_id = user_id
        self.food_id = food_id
        self.WhetherLike = WhetherLike


class UserCate(db.Model):
    __tablename__ = "UserCate"
    user_id = db.Column(db.Integer, db.ForeignKey("UserInfo.UserId"), primary_key=True)
    cate_id = db.Column(db.Integer, db.ForeignKey("CateInfo.id"), primary_key=True)
    cusLikeOrNot = db.Column(db.Boolean)

    def __init__(self, user_id, cate_id, cusLikeOrNot):
        self.user_id = user_id
        self.cusLikeOrNot = cusLikeOrNot
        self.cate_id = cate_id


class TagInfo(db.Model):
    __tablename__ = "TagInfo"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class ConstitutionInfo(db.Model):
    __tablename__ = "ConstitutionInfo"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


db.create_all()


def create_user(phone, password):
    user = UserInfo(phone, password)
    db.session.add(user)
    cates = CateInfo.query.all()
    foods = FoodInfo.query.all()
    for cate in cates:
        user_cate_new = UserCate(user_id=user.UserId, cate_id=cate.id, cusLikeOrNot=0)
        db.session.add(user_cate_new)
    for food in foods:
        user_food_new = UserFood(user_id=user.UserId, food_id=food.FoodId, WhetherLike=0)
        db.session.add(user_food_new)
    try:
        db.session.commit()
    except BaseException:
        return 0
    else:
        return user.UserId


def check_registered(phone):
    have_registed = UserInfo.query.filter_by(user_account=phone).all()
    if have_registed.__len__() is not 0:
        return True
    else:
        return False


@app.route('/')
def server_test():
    return 'This server is running...'


@app.route('/API/User/MailRegister', methods=['POST'])
def register():
    phone = request.form.get('Phone', 0)
    password = security.hashed_login_pwd(request.form.get('PassWord', 0))
    # password = request.form.get('PassWord', 0)
    if check_registered(phone):
        return jsonify({'Message': 'This phone number has been registered already, please use another phone number'}), \
               500

    # Use phone number as the user's account
    uid = create_user(phone, password)
    if uid == 0:
        return jsonify({'Message': 'Register failed, please check your information'}), 500

    return jsonify({'HttpCode': 200, 'ListData': [{'UserId': uid}], 'Message': 'Register success'})


@app.route('/API/User/Login', methods=['POST'])
def login():
    phone = request.form.get('UserPhone', 0)
    password = security.hashed_login_pwd(request.form.get('UserPassword', 0))
    if not check_registered(phone):
        return jsonify({'Message': 'This phone number has not been registered, please register at first'}), 500
    else:
        check_account = UserInfo.query.filter_by(user_account=phone, user_password=password).all()
        if check_account.__len__() is not 0:
            user_info = [check_account[0].serialize()]
            return jsonify({'HttpCode': 200, 'Message': 'Login success', 'ListData': user_info})
        else:
            return jsonify({'Message': 'Login failed, please check your phone number and password'}), 500


@app.route('/API/Question/GetQuestionExpressList', methods=['GET'])
def question_list():
    list_data = [{"QuestionId": 1, "QuestionContent": "您的饮食目标是？", "Options":
        [{"OptionId":1,"OptionContent":"确保日常饮食三餐规律和营养均衡"},
         {"OptionId":2,"OptionContent":"健身增肌"},
         {"OptionId":3,"OptionContent":"减脂瘦身"},
         {"OptionId":4,"OptionContent":"增加体重"}]},
                 {"QuestionId": 2, "QuestionContent": "您的精神状况如何，有如下状况吗？", "Options":
                     [{"OptionId":5,"OptionContent":"情绪稳定，性格平和"},
                      {"OptionId":6,"OptionContent":"敏感喜欢猜忌"},
                      {"OptionId":7,"OptionContent":"经常闷闷不乐"},
                      {"OptionId":8,"OptionContent":"多愁善感，焦虑不安"},
                      {"OptionId":9,"OptionContent":"精神总是紧张"},
                      {"OptionId":10,"OptionContent":"容易疲劳"},
                      {"OptionId":11,"OptionContent":"没有或不知道"}]},
                 {"QuestionId":3,"QuestionContent":"您的大小便状况如何？有如下状况吗？","Options":
                     [{"OptionId":12,"OptionContent":"便秘或大便干燥"},
                      {"OptionId":13,"OptionContent":"大便溏薄或者黏腻、不成形"},
                      {"OptionId":14,"OptionContent":"喝了冰的东西容易腹泻"},
                      {"OptionId":15,"OptionContent":"没有或不知道"}]},
                 {"QuestionId":4,"QuestionContent":"您的五官状况如何，有如下状况吗？","Options":
                     [{"OptionId":16,"OptionContent":"眼睛经常出现红疹发痒和血丝"},
                      {"OptionId":17,"OptionContent":"经常生痤疮"},
                      {"OptionId":18,"OptionContent":"嘴里有异味"},
                      {"OptionId":19,"OptionContent":"经常长痘痘"},
                      {"OptionId":20,"OptionContent":"女性白带颜色发黄"},
                      {"OptionId":21,"OptionContent":"容易呼吸短促，接不上气"},
                      {"OptionId":22,"OptionContent":"没有或不知道"}]},
                 {"QuestionId":5,"QuestionContent":"您的皮肤状况如何，有如下状况吗？","Options":
                     [{"OptionId":23,"OptionContent":"皮肤一抓就红"},
                      {"OptionId":24,"OptionContent":"容易出汗"},
                      {"OptionId":25,"OptionContent":"面颊潮红或偏红"},
                      {"OptionId":26,"OptionContent":"肌肤不滋润，干燥"},
                      {"OptionId":27,"OptionContent":"没有或不知道"}]},
                 {"QuestionId":6,"QuestionContent":"您的适应能力抵抗力如何？","Options":
                     [{"OptionId":28,"OptionContent":"无故鼻塞流涕、打喷嚏"},
                      {"OptionId":29,"OptionContent":"容易过敏"},
                      {"OptionId":30,"OptionContent":"身体莫名其妙疼痛"},
                      {"OptionId":31,"OptionContent":"经常手脚发凉"},
                      {"OptionId":32,"OptionContent":"没有或不知道"}]},
                 {"QuestionId":7,"QuestionContent":"您身体的整体状况如何？","Options":
                     [{"OptionId":33,"OptionContent":"精力充沛"},
                      {"OptionId":34,"OptionContent":"面色红润、目光有神"},
                      {"OptionId":35,"OptionContent":"食欲很好"},
                      {"OptionId":36,"OptionContent":"容易感冒"},
                      {"OptionId":37,"OptionContent":"经常头昏眼花"},
                      {"OptionId":38,"OptionContent":"经常上火，口干舌燥"},
                      {"OptionId":39,"OptionContent":"经常腰酸腿软"},
                      {"OptionId":40,"OptionContent":"没有或不知道"}]},
                 {"QuestionId":8,"QuestionContent":"您还有哪些状况？","Options":
                     [{"OptionId":41,"OptionContent":"总是觉得很累"},
                      {"OptionId":42,"OptionContent":"特别容易掉头发"},
                      {"OptionId":43,"OptionContent":"脸色晦暗、长色斑"},
                      {"OptionId":44,"OptionContent":"额头总是油油的"},
                      {"OptionId":45,"OptionContent":"嘴巴里有黏的感觉"},
                      {"OptionId":46,"OptionContent":"没有或不知道"}]}]
    return jsonify({'HttpCode': 200, 'Message': 'Get questions list success', 'ListData': list_data})


@app.route('/API/Question/GetQuestionProfessionList', methods=['POST'])
def question_list_pro():
    uid = request.form.get('UserId', 0)

    list_data= [{"QuestionId":9,"QuestionContent":"您手脚发凉吗？","Options":
        [{"OptionId":47,"OptionContent":"完全不"},
         {"OptionId":48,"OptionContent":"有一点"},
         {"OptionId":49,"OptionContent":"非常"}]},
                {"QuestionId":10,"QuestionContent":"您感到怕冷、衣服比别人穿得多吗？","Options":
                    [{"OptionId":50,"OptionContent":"完全不"},
                     {"OptionId":51,"OptionContent":"有一点"},
                     {"OptionId":52,"OptionContent":"非常"}]},
                {"QuestionId": 11, "QuestionContent": "您感到手脚心发热吗？", "Options":
                    [{"OptionId": 53, "OptionContent": "完全不"},
                     {"OptionId": 54, "OptionContent": "有一点"},
                     {"OptionId": 55, "OptionContent": "非常"}]},
                {"QuestionId": 12, "QuestionContent": "您感到口干咽燥、总想喝水吗?", "Options":
                    [{"OptionId": 56, "OptionContent": "完全不"},
                     {"OptionId": 57, "OptionContent": "有一点"},
                     {"OptionId": 58, "OptionContent": "非常"}]},
                {"QuestionId": 13, "QuestionContent": "您容易气短（呼吸短促、接不上气）吗", "Options":
                    [{"OptionId": 59, "OptionContent": "完全不"},
                     {"OptionId": 60, "OptionContent": "有一点"},
                     {"OptionId": 61, "OptionContent": "非常"}]},
                {"QuestionId": 14, "QuestionContent": "您容易头晕或站起来时晕眩吗？", "Options":
                    [{"OptionId": 62, "OptionContent": "完全不"},
                     {"OptionId": 63, "OptionContent": "有一点"},
                     {"OptionId": 64, "OptionContent": "非常"}]},
                {"QuestionId": 15, "QuestionContent": "您感到身体沉重不轻松或不爽快吗？", "Options":
                    [{"OptionId": 65, "OptionContent": "完全不"},
                     {"OptionId": 66, "OptionContent": "有一点"},
                     {"OptionId": 67, "OptionContent": "非常"}]},
                {"QuestionId": 16, "QuestionContent": "您平时痰多，特别咽喉部总感到有痰堵着吗？", "Options":
                    [{"OptionId": 68, "OptionContent": "完全不"},
                     {"OptionId": 69, "OptionContent": "有一点"},
                     {"OptionId": 70, "OptionContent": "非常"}]},
                {"QuestionId": 17, "QuestionContent": "您感到口苦或嘴里有异味吗？", "Options":
                    [{"OptionId": 71, "OptionContent": "完全不"},
                     {"OptionId": 72, "OptionContent": "有一点"},
                     {"OptionId": 73, "OptionContent": "非常"}]},
                {"QuestionId": 18, "QuestionContent": "您容易生痤疮或疮疖吗？", "Options":
                    [{"OptionId": 74, "OptionContent": "完全不"},
                     {"OptionId": 75, "OptionContent": "有一点"},
                     {"OptionId": 76, "OptionContent": "非常"}]},
                {"QuestionId": 19, "QuestionContent": "您的皮肤在不知不觉中出现青紫瘀斑（皮下出血）吗？", "Options":
                    [{"OptionId": 77, "OptionContent": "完全不"},
                     {"OptionId": 78, "OptionContent": "有一点"},
                     {"OptionId": 79, "OptionContent": "非常"}]},
                {"QuestionId": 20, "QuestionContent": "您面色晦暗或容易出现褐斑吗？", "Options":
                    [{"OptionId": 77, "OptionContent": "完全不"},
                     {"OptionId": 78, "OptionContent": "有一点"},
                     {"OptionId": 79, "OptionContent": "非常"}]},
                {"QuestionId": 21, "QuestionContent": "您没有感冒时也会打喷嚏吗？", "Options":
                    [{"OptionId": 77, "OptionContent": "完全不"},
                     {"OptionId": 78, "OptionContent": "有一点"},
                     {"OptionId": 79, "OptionContent": "非常"}]},
                {"QuestionId": 22, "QuestionContent": "您有因季节变化、温度变化或异味等原因而咳喘的现象吗？", "Options":
                    [{"OptionId": 77, "OptionContent": "完全不"},
                     {"OptionId": 78, "OptionContent": "有一点"},
                     {"OptionId": 79, "OptionContent": "非常"}]},
                {"QuestionId": 23, "QuestionContent": "您多愁善感、感情脆弱吗？", "Options":
                    [{"OptionId": 77, "OptionContent": "完全不"},
                     {"OptionId": 78, "OptionContent": "有一点"},
                     {"OptionId": 79, "OptionContent": "非常"}]},
                {"QuestionId": 24, "QuestionContent": "您咽喉部有异物感，且吐之不出、咽之不下吗？", "Options":
                    [{"OptionId": 77, "OptionContent": "完全不"},
                     {"OptionId": 78, "OptionContent": "有一点"},
                     {"OptionId": 79, "OptionContent": "非常"}]},
                {"QuestionId": 25, "QuestionContent": "您精力充沛吗？", "Options":
                    [{"OptionId": 77, "OptionContent": "完全不"},
                     {"OptionId": 78, "OptionContent": "有一点"},
                     {"OptionId": 79, "OptionContent": "非常"}]},
                {"QuestionId": 26, "QuestionContent": "您能适应外界自然和社会环境的变化吗？", "Options":
                    [{"OptionId": 77, "OptionContent": "完全不"},
                     {"OptionId": 78, "OptionContent": "有一点"},
                     {"OptionId": 79, "OptionContent": "非常"}]}]
    return jsonify({'HttpCode': 200, 'Message': 'Get questions list success', 'ListData': list_data})


########### Need improvement ###########
@app.route('/API/Question/GetSubmitExpressQuestion', methods=['POST'])
def answer_process():
    uid = request.form.get('UserId', 0)
    answer = request.form.get('answer', 0)
    print(answer, file=sys.stderr)
    print(type(answer), file=sys.stderr)
    body_model = '特禀体质的人会出现打喷嚏、流清涕，就是因为卫气虚不能抵御外邪所致。中医认为，“肾为先天之本”，特禀质养生时就应以健脾、补肾气为主，以增强卫外功能。特禀质，这是一类体质特殊的人群。 ⑤对外界环境适应能力：适应能力差，如过敏体质者对过敏季节适应能力差，易引发宿疾。 体质分析 由于先天禀赋不足、遗传等因素，或环境因素，药物因素等的不同影响，故特异质的形体特征、心理特征、常见表现、发病倾向等方面存在诸多差异，病机各异。'

    user = UserInfo.query.get(uid)
    user.constitution = "特禀质"
    db.session.add(user)
    try:
        db.session.commit()
    except BaseException:
        return jsonify({'HttpCode': 500, 'Message': 'Server database updating error'}), 500
    else:
        return jsonify({'HttpCode': 200, 'Model1': body_model})


########### Need improvement,may not need response ###########
@app.route('/API/Question/GetSubmitQuestion', methods=['POST'])
def professional_answer_process():
    uid = request.form.get('UserId', 0)
    answer = request.form.get('answer', 0)
    print(answer, file=sys.stderr)
    print(type(answer), file=sys.stderr)

    user = UserInfo.query.get(uid)
    answer_list = answer.split('|')
    for i,answer in enumerate(answer_list):
        if int(answer.split(',')[1]) >= 2:
            if i == 0 or i == 1:
                body_model = '阳虚质'
                break
            elif i == 2 or i == 3:
                body_model = '阴虚质'
                break
            elif i == 4 or i == 5:
                body_model = '气虚质'
                break
            elif i == 6 or i == 7:
                body_model = '痰湿质'
                break
            elif i == 8 or i == 9:
                body_model = '湿热质'
                break
            elif i == 10 or i == 11:
                body_model = '血瘀质'
                break
            elif i == 12 or i == 13:
                body_model = '特禀质'
                break
            elif i == 14 or i == 15:
                body_model = '气郁质'
                break
            elif i == 16 or i == 17:
                body_model = '平和质'
                break
            else:
                body_model = user.constitution
                break

    #body_model = '特禀体质的人会出现打喷嚏、流清涕，就是因为卫气虚不能抵御外邪所致。中医认为，“肾为先天之本”，特禀质养生时就应以健脾、补肾气为主，以增强卫外功能。特禀质，这是一类体质特殊的人群。 ⑤对外界环境适应能力：适应能力差，如过敏体质者对过敏季节适应能力差，易引发宿疾。 体质分析 由于先天禀赋不足、遗传等因素，或环境因素，药物因素等的不同影响，故特异质的形体特征、心理特征、常见表现、发病倾向等方面存在诸多差异，病机各异。'
    if body_model == '阳虚质':
        body_model = '气郁质'
    if body_model == '阴虚质':
        body_model = '气郁质'
    if body_model == '气虚质':
        body_model = '气郁质'
    if body_model == '痰湿质':
        body_model = '湿热质'

    user.constitution = body_model
    db.session.add(user)
    try:
        db.session.commit()
    except BaseException:
        return jsonify({'HttpCode': 500, 'Message': 'Server database updating error'}), 500
    else:
        return jsonify({'HttpCode': 200, 'Model1': body_model})


@app.route('/API/User/UserScoreInfo', methods=['POST'])
def user_info():
    uid = request.form.get('UserId', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    user = UserInfo.query.get(uid)
    constitution = user.constitution
    score = user.score
    name = user.name

    return jsonify({'HttpCode': 200, 'Model1': {'Current_Score': score, 'Next_Score': 9, 'Current_Name': name}})


@app.route('/API/User/SetUserBodyInfo', methods=['POST'])
def set_body_info():
    uid = request.form.get('UserId', 0)
    sex = request.form.get('UserSex', 0)
    birth_day = request.form.get('UserBirthTime', 0)
    height = request.form.get('UserHeight', 0)
    weight = request.form.get('UserWeight', 0)
    lab_inten = request.form.get('labInten', 0)

    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    user = UserInfo.query.get(uid)
    if sex == "true":
        user.sex = True
    else:
        user.sex = False
    new_birthday = datetime.strptime(birth_day,'%Y-%m-%d')
    user.BirthDay = new_birthday
    today = datetime.today()
    user.age = int((today - new_birthday).days/365)
    user.height = int(height)
    user.weight = int(weight)
    user.labourIntensity = int(lab_inten)
    db.session.add(user)
    try:
        db.session.commit()
    except BaseException:
        return jsonify({'HttpCode': 500, 'Message': 'Server database updating error'}), 500
    else:
        user_new_info = [user.serialize()]
        return jsonify({'HttpCode': 200, 'Message': 'Login success', 'ListData': user_new_info})


@app.route('/API/User/SetUserInfo', methods=['POST'])
def set_user_info():
    uid = request.form.get('UserId', 0)
    name = request.form.get('UserName', 0)

    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    user = UserInfo.query.get(uid)
    user.name = name
    db.session.add(user)
    try:
        db.session.commit()
    except BaseException:
        return jsonify({'HttpCode': 500, 'Message': 'Server database updating error'}), 500
    else:
        user_new_info = [user.serialize()]
        return jsonify({'HttpCode': 200, 'Message': 'Login success', 'ListData': user_new_info})


@app.route('/API/User/GetUserBodyInfo', methods=['POST'])
def get_body_info():
    uid = request.form.get('UserId', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    user = UserInfo.query.get(uid)
    user_new_info = [user.serialize()]
    return jsonify({'HttpCode': 200, 'Message': 'Get body information successfully', 'ListData': user_new_info})


# @app.route('/API/Sport/UpLoadSportInfo', methods=['POST'])
# def set_sport():
#     uid = request.form.get('UserId', 0)
#     steps = request.form.get('Steps', 0)
#     if uid == 0:
#         return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
#     user = UserInfo.query.get(uid)
#     user.sport


@app.route('/API/Restaurant/TitlePage', methods=['POST'])
def get_title_page():
    uid = request.form.get('UserId', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500

    user = UserInfo.query.get(uid)
    user_constitution = user.constitution
    #articles = ArticleInfo.query.filter_by(tag=user_constitution).all()
    articles = ArticleInfo.query.all()
    cates = CateInfo.query.all()
    recipes = RecipeInfo.query.filter_by(tag=user_constitution).all()

    list_data1 = []
    list_data2 = []
    list_data3 = []
    for cate in cates:
        list_data1.append(cate.serialize())
    for recipe in recipes:
        list_data2.append(recipe.serialize())
    for article in articles:
        list_data3.append(article.serialize())
    #list_data1 = [{"id":1,"name":"乐惠（同济店）","titleImage":"https://ws4.sinaimg.cn/large/006tKfTcly1g1du9wdjo0j30jg09q75e.jpg","address":"上海市嘉定区安亭镇曹安公路4800号嘉实花园A区4号楼SP10","phone":"13817873578","category":"5","sales":654,"consumption":321,"discount":"满10减2，满13减3","distance":180},{"id":2,"name":"梦飨餐厅","titleImage":"https://ws3.sinaimg.cn/large/006tKfTcly1g1dvrddlzgj30el0jggmc.jpg","address":"嘉松北路6128号S146-148","phone":"18621631527","category":"5","sales":2,"consumption":2,"discount":"满55减5，满100减8","distance":240},{"id":3,"name":"臻食","titleImage":"https://ws4.sinaimg.cn/large/006tKfTcly1g1dwghuzzxj30jg0el0to.jpg","address":"嘉松北路6130弄嘉实生活广场2楼","phone":"021-59949050","category":"5","sales":111,"consumption":22,"discount":"学生全场88折","distance":909},{"id":4,"name":"小朵颐（同济大学）","titleImage":"https://ws4.sinaimg.cn/large/006tKfTcly1g1dwkbuw3wj30jg0el0tm.jpg","address":"同济新天地S161","phone":"13162937158","category":"5","sales":1111,"consumption":1,"discount":"满15减9，满36减12","distance":232},{"id":5,"name":"酸菜鱼馆（同济店）","titleImage":"https://ws2.sinaimg.cn/large/006tKfTcly1g1dwrv2p0gj30jg0el407.jpg","address":"同济大学新天地商业街2楼","phone":"18262069803","category":"5","sales":12,"consumption":12,"discount":"满15减9，满45减11","distance":233},{"id":6,"name":"瓦罐煨汤（同济店）","titleImage":"https://ws2.sinaimg.cn/large/006tKfTcly1g1dwvqgfx6j306x06xglo.jpg","address":"同济大学新天地广场2层","phone":"13301605235","category":"3","sales":88811,"consumption":251,"discount":"满20减2","distance":220},{"id":7,"name":"皖南小厨","titleImage":"https://ws3.sinaimg.cn/large/006tKfTcly1g1dx1gfg20j308y0byq3c.jpg","address":"安亭镇绿苑路634号1层","phone":"15800904776","category":"5","sales":1,"consumption":2,"discount":"满35赠啤酒一份","distance":712},{"id":8,"name":"Sally墨西哥风味快餐","titleImage":"https://ws3.sinaimg.cn/large/006tKfTcly1g1dxgz7m40j30u00tse81.jpg","address":"嘉松北路6130弄198号S7-102","phone":"18516059807","category":"5","sales":111,"consumption":222,"discount":"满30减4，满40减7","distance":476},{"id":9,"name":"壹粥壹煲","titleImage":"https://ws2.sinaimg.cn/large/006tKfTcly1g1dxmhlx8bj30u00s2wyb.jpg","address":"上海市嘉定区江桥镇星华公路1574号1层","phone":"13501646449","category":"5","sales":111,"consumption":2,"discount":"满25减14，满45减20","distance":773}]
    #list_data2 = [{"id":1, "name":"韭菜鸡蛋盒子","titleImage":"http://images.meishij.net/p/20141124/513abccfb30d638e0ad5ce5d5c5edf7e.jpg","ConstitutionPercentage":75,"sales":11,"price":"11.00","Tags":["煎","咸煎味"],"Restaurant_Name":"小朵颐","Restaurant_Address":"嘉定校区新天地","distance":232,"category":"5"},{"id":9,"name":"糖醋虎皮尖椒","titleImage":"http://site.meishij.net/r/184/180/4420184/s4420184_147608026557745.jpg","ConstitutionPercentage":30,"sales":22,"price":"20.00","Tags":["煎","酸甜味"],"Restaurant_Name":"酸菜鱼（同济店）","Restaurant_Address":"嘉定校区新天地2楼","distance":541,"category":"5"},{"id":1,"name":"胡萝卜土豆炖牛肉","titleImage":"http://images.meishij.net/p/20130620/37c5e6dc7a6bbdf1dadc28e8ffb1cfb8.jpg","ConstitutionPercentage":65,"sales":12,"price":"38.00","Tags":["炖","咸鲜味"],"Restaurant_Name":"梦飨餐厅","Restaurant_Address":"嘉定校区新天地2楼","distance":3843,"category":"3"},{"id":5,"name":"山药煲","titleImage":"http://images.meishij.net/p/20130613/92b3f0ae16bf564d867dfad2cdf16504.jpg","ConstitutionPercentage":30,"sales":99,"price":"18.00","Tags":["煲","咸鲜味"],"Restaurant_Name":"瓦罐煨汤","Restaurant_Address":"嘉定校区新天地2楼","distance":220,"category":"5"},{"id":6,"name":"羊肉炖萝卜","titleImage":"http://images.meishij.net/p/20130605/9d823c2e9bd52869b9629c799c007fca.jpg","ConstitutionPercentage":50,"sales":11,"price":"47.00","Tags":["红烧","咸鲜味"],"Restaurant_Name":"臻食","Restaurant_Address":"嘉实广场2楼","distance":909,"category":"5"}]
    #list_data3 = [{"ArticleId":103,"title":"缓解痉挛吃黄酒煮猪蹄","content":'null',"TitleImage":"http://www.foodwang.com/uploads/allimg/190125/1-1Z125164934964.jpg","tags":["猪蹄","缓解痉挛"],"ConstitutionPercentage":30,"cilckCount":141,"loveCount":35,"aTime":"2017-07-27T16:32:00","url":"http://www.foodwang.com/dapei/201901/62480.html","PointPraise":'true'},{"ArticleId":104,"title":"体寒喝姜水、吃红枣？不如吃高蛋白食物！","content": 'null',"TitleImage":"http://www.foodwang.com/uploads/allimg/190124/1-1Z124121519B6.jpg","tags":["寒性体质","高蛋白"],"ConstitutionPercentage":50,"cilckCount":31,"loveCount":4,"aTime":"2017-07-27T16:31:00","url":"http://www.foodwang.com/dapei/chishenme/2019/0124/62476.html","PointPraise":'true'},{"ArticleId":147,"title":"压力山大？试试这些“快乐食物”","content":'null',"TitleImage":"http://www.foodwang.com/uploads/allimg/180923/1-1P923142054934.jpg","tags":["减压","色氨酸","钙","镁"],"ConstitutionPercentage":30,"cilckCount":38,"loveCount":4,"aTime":"2017-07-27T15:21:00","url":"http://www.foodwang.com/dapei/chishenme/2018/0923/62333.html","PointPraise":'true'},{"ArticleId":149,"title":"缓解焦虑情绪要多吃这几种食物","content":'null',"TitleImage":"http://www.foodwang.com/uploads/allimg/170818/1-1FQQ33HM33.jpg","tags":["减压","焦虑","红枣","玫瑰花","羊心","大蒜","土豆"],"ConstitutionPercentage":50,"cilckCount":26,"loveCount":2,"aTime":"2017-07-27T12:48:00","url":"http://www.foodwang.com/dapei/chishenme/2015/1111/58554.html","PointPraise":'true'}]
    list_data4 = []
    return jsonify({'HttpCode': 200, 'Message': 'Get title information successfully', 'ListData': list_data1, 'ListData2': list_data2, 'ListData3': list_data3, 'ListData4': list_data4})


@app.route('/API/DataDictionary/Cate', methods=['POST'])
def get_cate_type():
    type_like = request.form.get('Type_Like', 0)
    list_data = [{"id":1,"typeValue":"快餐"},{"id":2,"typeValue":"中餐"},{"id":3,"typeValue":"西餐"}]
    return jsonify({'HttpCode': 200, 'Message': 'Get cate type successfully', 'ListData': list_data})


@app.route('/API/Restaurant/GetRestaurantInfoById', methods=['POST'])
def get_cate_info():
    uid = request.form.get('UserId', 0)
    cid = request.form.get('id', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    like = UserCate.query.filter_by(user_id=uid).filter_by(cate_id=cid).all()
    cate = CateInfo.query.get(cid)
    cate_info = cate.serialize()
    cate_info['images'] = [cate_info['titleImage']]
    cate_info['cusLikeOrNot'] = like[0].cusLikeOrNot
    return jsonify({'HttpCode': 200, 'Message': 'Get cate information successfully', 'ListData': [cate_info]})


@app.route('/API/Recipe/RecipeItemInfo', methods=['POST'])
def get_recipe_item():
    rid = request.form.get('RecipeId', 0)
    uid = request.form.get('UserId', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    if rid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'Recipe id error'}), 500
    recipe = RecipeInfo.query.get(rid)
    recipe_info = recipe.serialize()
    foods = recipe_info['foodRecipe'][0]['ListFood']
    new_foods = []
    for food in foods:
        food_id = food['FoodId']
        user_food = UserFood.query.filter_by(user_id=uid).filter_by(food_id=food_id).all()
        if len(user_food) == 0:
            food['WhetherLike'] = 0
        else:
            food['WhetherLike'] = user_food[0].WhetherLike
            print(type(user_food[0].WhetherLike), file=sys.stderr)
        new_foods.append(food)
    recipe_info['foodRecipe'][0]['ListFood'] = new_foods

    return jsonify({'HttpCode': 200, 'Message': 'Get recipe information successfully', 'ListData': [recipe_info]})


@app.route('/API/Score/GetClickScore', methods=['POST'])
def get_click_score():
    uid = request.form.get('UserId', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    model1 = {"Score":1.1,"ListId":",20","ScoreType":"sleep","ScoreContent":None}
    model2 = {"Score":1.1,"ListId":",20","ScoreType":"sleep","ScoreContent":None}
    model3 = {"Score":1.1,"ListId":",20","ScoreType":"sleep","ScoreContent":None}

    return jsonify({'HttpCode': 200, 'Message': 'Get leaf information successfully', 'Model1': model1, 'Model2': model2, 'Model3': model3})


@app.route('/API/Sport/GetSportList', methods=['POST'])
def get_sport_list():
    uid = request.form.get('UserId', 0)
    data_type = request.form.get('dateType', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    if uid == 1:
        sport_history = [{"date": "3.26", "steps": 6032}, {"date": "3.27", "steps": 9750}, {"date": "3.28", "steps": 10235},
                         {"date": "3.29", "steps": 8764}, {"date": "3.30", "steps": 9344}, {"date": "3.31", "steps": 7943},
                         {"date": "4.1", "steps": 13431}, {"date": "4.2", "steps": 3123}, {"date": "4.3", "steps": 2823}]
    else:
        sport_history = [{"date": "3.26", "steps": 0}, {"date": "3.27", "steps": 0}, {"date": "3.28", "steps": 0},
                         {"date": "3.29", "steps": 0}, {"date": "3.30", "steps": 0}, {"date": "3.31", "steps": 0},
                         {"date": "4.1", "steps": 0}, {"date": "4.2", "steps": 0}, {"date": "4.3", "steps": 0}]

    return jsonify({'HttpCode': 200, 'Message': 'Get sport information successfully', 'ListData': sport_history})


@app.route('/API/Score/GetScoreList', methods=['POST'])
def get_score_list():
    uid = request.form.get('UserId', 0)
    page_no = request.form.get('PageNo', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    datetime.today()
    score_list = [{'ScoreId': 3, 'ScoreType': 'sleep', 'ScoreNum': 0.5, 'Time': datetime.isoformat(datetime.today()), 'Content': '在23点之前睡觉'}]

    return jsonify({'HttpCode': 200, 'Message': 'Get sport information successfully', 'ListData': score_list})


@app.route('/API/Article/GetArticleListInfo', methods=['POST'])
def get_article_list():
    uid = request.form.get('Id', 0)
    page_no = request.form.get('PageNo', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    user = UserInfo.query.get(uid)
    user_constitution = user.constitution
    articles = ArticleInfo.query.filter_by(tag=user_constitution).all()

    list_data = []
    for article in articles:
        list_data.append(article.serialize())
    ################ Need improvement #########################
    list_data2 = [{'constitution': user_constitution, 'SuitEat': '杂粮，红肉', 'NotSuitEat': '少吃辛辣，刺激类食物'}]

    return jsonify({'HttpCode': 200, 'Message': 'Get article information successfully', 'ListData': list_data, 'ListData2': list_data2})


@app.route('/API/Article/GetArticleItemInfo', methods=['POST'])
def get_article_info():
    uid = request.form.get('UserId', 0)
    aid = request.form.get('Id', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    article = ArticleInfo.query.get(aid)
    article_info = article.serialize()

    return jsonify({'HttpCode': 200, 'Message': 'Get article item information successfully', 'ListData': [article_info]})


@app.route('/API/Recipe/RecipeListInfoByDRId', methods=['POST'])
def get_recipe_by_cate():
    uid = request.form.get('UserId', 0)
    cid = request.form.get('id', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    recipes = RecipeInfo.query.filter_by(RestaurantId=cid).all()
    list_data = []
    for recipe in recipes:
        recipe_info_json = recipe.serialize()
        food_list = recipe_info_json['foodRecipe'][0]['ListFood']
        food_str = ""
        for food in food_list:
            food_str = food_str + food['FoodName'] + ' '+str(food['FoodWeight'])+' '

        recipe_info_json['foodRecipe'][0]['ListFood'] = food_str
        list_data.append(recipe_info_json)

    return jsonify({'HttpCode': 200, 'Message': 'Get recipe information successfully', 'ListData': list_data})


@app.route('/API/Restaurant/GetRestaurantListInfo', methods=['POST'])
def get_cate_list():
    group_by = request.form.get('GroupBy', 0)  # Distance, SalesValume
    page_no = request.form.get('PageNo', 0)
    type_value = request.form.get('TypeValue', 0)  # 1,2,3

    cates = CateInfo.query.all()
    if group_by == 'Distance':
        cates = CateInfo.query.order_by("distance").all()
    elif group_by == 'SalesValume':
        cates = CateInfo.query.order_by('sales desc').all()
    elif group_by == 'Type':
        cates = CateInfo.query.filter_by(category=type_value).all()

    list_data = []
    for cate in cates:
        list_data.append(cate.serialize())

    return jsonify({'HttpCode': 200, 'Message': 'Get cate list information successfully', 'ListData': list_data})


@app.route('/API/Recipe/RecipeListByGPS', methods=['POST'])
def get_cate_list_gps():
    group_by = request.form.get('GroupBy', 0)  # Distance, SalesValume
    page_no = request.form.get('PageNo', 0)
    type_value = request.form.get('TypeValue', 0)  # 1,2,3

    cates = CateInfo.query.all()
    if group_by == 'Distance':
        cates = CateInfo.query.order_by("distance").all()
    elif group_by == 'SalesValume':
        cates = CateInfo.query.order_by('sales desc').all()
    elif group_by == 'Type':
        cates = CateInfo.query.filter_by(category=type_value).all()

    list_data = []
    for cate in cates:
        recipes = RecipeInfo.query.filter_by(RestaurantId=cate.id).all()
        for recipe in recipes:
            list_data.append(recipe.serialize())

    return jsonify({'HttpCode': 200, 'Message': 'Get cate list information successfully', 'ListData': list_data})


@app.route('/API/User/SelectUserPreference', methods=['POST'])
def get_user_prefer():
    uid = request.form.get('UserId', 0)
    type_like = request.form.get('Type_Like', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    list_data = []
    if type_like == "foodlike":
        foods = UserFood.query.filter_by(user_id=uid).filter_by(WhetherLike=2).all()
    elif type_like == "foodunlike":
        foods = UserFood.query.filter_by(user_id=uid).filter_by(WhetherLike=1).all()
    for food in foods:
        food_id = food.food_id
        food_info = FoodInfo.query.get(food_id).serialize()
        food_info['WhetherLike'] = food.WhetherLike
        list_data.append(food_info)

    return jsonify({'HttpCode': 200, 'Message': 'Get food like information successfully', 'ListData': list_data})


@app.route('/API/Restaurant/CustomerLikeOrNot', methods=['POST'])
def sef_customer_like():
    # "Type_Like", "restlike");
    # map.put("OtherId", OtherId);
    # map.put("Opertion", Opertion);
    # map.put("UserId",
    type_like = request.form.get('Type_Like', 0)
    operation = request.form.get('Opertion')
    other_id = request.form.get('OtherId')
    uid = request.form.get('UserId')
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    if type_like == 'foodlike' or type_like == 'foodunlike':
        type_like = 2 if request.form.get('Type_Like', 0) == 'foodlike' else 1
        user_food = UserFood.query.filter_by(user_id=uid).filter_by(food_id=other_id).all()
        if len(user_food) == 0 and operation == 'Insert':
            new_user_food = UserFood(user_id=uid, food_id=other_id, WhetherLike=type_like)
            db.session.add(new_user_food)
        if operation == 'Insert':
            user_food[0].WhetherLike = type_like
            db.session.add(user_food[0])
        if operation == 'Delete':
            user_food[0].WhetherLike = 0
            db.session.add(user_food[0])
    elif type_like == 'restlike':
        # print(uid, file=sys.stderr)
        # print(other_id,file=sys.stderr)
        user_cate = UserCate.query.filter_by(user_id=uid).filter_by(cate_id=other_id).all()
        if len(user_cate) == 0:
            return jsonify({'HttpCode': 500, 'Message': 'Do not find the cate information!'}), 500
        # print(type(user_cate[0]), file=sys.stderr)
        user_cate[0].cusLikeOrNot = not user_cate[0].cusLikeOrNot
        db.session.add(user_cate[0])

    db.session.commit()

    return jsonify({'HttpCode': 200, 'Message': 'Change food like information successfully'})


@app.route('/API/Restaurant/UserPreferenceRest', methods=['POST'])
def get_user_prefer_cate():
    uid = request.form.get('UserId', 0)
    page_no = request.form.get('PageNo', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    user_cates = UserCate.query.filter_by(user_id=uid).filter_by(cusLikeOrNot=1).all()
    list_data = []
    for user_cate in user_cates:
        cate_id = user_cate.cate_id
        cate_info = CateInfo.query.get(cate_id).serialize()
        list_data.append(cate_info)

    return jsonify({'HttpCode': 200, 'Message': 'Get user like cates information successfully','ListData': list_data})


@app.route('/API/Recipe/RecipeItemInfoForPay', methods=['POST'])
def pay_recipe():
    uid = request.form.get('UserId', 0)
    rid = request.form.get('RecipeId', 0)
    if uid == 0:
        return jsonify({'HttpCode': 500, 'Message': 'User id error'}), 500
    recipe = RecipeInfo.query.get(rid)
    list_data = [recipe.serialize()]
    cid = recipe.RestaurantId
    cate = CateInfo.query.get(cid)
    list_data2 = [cate.serialize()]

    return jsonify({'HttpCode': 200, 'Message': 'Get payment information successfully', 'ListData': list_data, 'ListData2': list_data2})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=580)