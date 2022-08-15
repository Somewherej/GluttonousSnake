import pgzrun
import random
import numpy as np

txt = open('rank', 'r')        # 打开最佳记录存档文件
bestScore = txt.readline()     # 读取字符串
bestScore = int(bestScore)         # 将最最佳成绩转换为整型
txt.close()                    # 关闭文件

#变量初始化
moveDirection = 'up'  # 控制小蛇运动方向
isRun = True          # 游戏是否运行   or 是否结束
newScore = 0          # 这次游戏蛇的长度
situation = 0         # 控制失败的情况(1:越界 2:碰到自身 3:碰到障碍物)
size = 20             # 小蛇方块的大小，20*20
WIDTH = 40*size       # 设置窗口的宽度 800
HEIGHT = 40*size      # 设置窗口的高度 800

#Actor 请换成你自己电脑图片的绝对路径
food = Actor('cookie.jpg')  # 导入食物方块图片
food.x = random.randint(10, 30)*size  # 食物方块图片的x坐标
food.y = random.randint(10, 30)*size  # 食物方块图片的y坐标

#Actor 请换成你自己电脑图片的绝对路径
endButton = Actor('结束.jpg')   # 导入暂停方块图片
endButton.x = WIDTH- 20   # 暂停方块图片的x坐标
endButton.y = 20           # 暂停方块图片的y坐标e

#Actor 请换成你自己电脑图片的绝对路径
obstacleHead = Actor('Brick.jpg')    # 导入障碍物图片
obstacleHead.x = random.randint(1, 30)*size          # 障碍物方块图片的x坐标
obstacleHead.y = random.randint(1, 30)*size         # 障碍物方块图片的y坐标
obstacles = []                       # 存储障碍物的列表
obstaclesX=[]                        # 储存障碍物x坐标的列表
obstaclesY=[]                        # 储存障碍物y坐标的列表
obstaclesX.append((obstacleHead.x)/size)    #对于这个obstaclesX和obstaclesY是为了保存每个障碍物对应x/size,y/size, 控制饼干不会和障碍物重叠
obstaclesY.append((obstacleHead.y)/size)
obstaclesX.append(20)   #排除障碍物出现在起点
obstaclesY.append(20)
obstacles.append(obstacleHead)
for i in range(15):                     #想难一点，你就在这里控制      障碍物的数量，障碍物的总数现在是15+1=16个
    newObstacle = Actor('Brick.jpg')  #Actor 请换成你自己电脑图片的绝对路径
    newObstacle.x = random.randint(1, 30)*size       # 障碍物方块图片的x坐标
    newObstacle.y = random.randint(1, 30)*size       # 障碍物方块图片的y坐标
    obstacles.append(newObstacle)                    # 把障碍物加入到列表中
    obstaclesX.append((newObstacle.x)/size)
    obstaclesY.append((newObstacle.y)/size)

#Actor 请换成你自己电脑图片的绝对路径
snakeHead = Actor('snake.jpg')                 # 导入蛇头方块图片
snakeHead.x = WIDTH/2                      # 蛇头方块图片的x坐标
snakeHead.y = HEIGHT/2                     # 蛇头方块图片的y坐标
Snake = []                                 # 存储蛇的列表
Snake.append(snakeHead)
for i in range(2):
    # Actor 请换成你自己电脑图片的绝对路径
    snakebody = Actor('snake.jpg')
    snakebody.x = Snake[i].x - size
    snakebody.y = Snake[i].y
    Snake.append(snakebody)




def draw():                    # 绘制模块，每帧重复执行
    screen.clear()             # 每帧清除屏幕，便于重新绘制
    for i in Snake:            # 绘制蛇
        i.draw()
    for i in obstacles:        # 绘制障碍物
        i.draw()
    food.draw()                # 食物的绘制
    endButton.draw()           # 结束按钮的绘制

    screen.draw.text("当前得分："+str(newScore), (360, 10), fontsize=20,
                     fontname='s', color='white')

    if isRun == False:                                 # isRun == False 表示程序不再运行
        screen.clear()  # 每帧清除屏幕，便于重新绘制
        ##Actor 请换成你自己电脑图片的绝对路径
        f = Actor('界面图片')
        f.draw()
        screen.draw.text("游戏结束！", (WIDTH/2-80, HEIGHT/2-100),fontsize=40, fontname='s', color='red')
        if(situation == 1):
            screen.draw.text("蛇超过边界", (355, 460), fontsize=20, fontname='s', color='red')
        if (situation == 2):
            screen.draw.text("蛇碰到自身", (360,  460), fontsize=20, fontname='s', color='red')
        if (situation == 3):
            screen.draw.text("蛇碰到障碍物", (355, 460), fontsize=20, fontname='s', color='red')
        if  bestScore < newScore :                     # 看看是否更新最长蛇的记录
                screen.draw.text("恭喜你打破了最佳记录", (310, 375), fontsize=20,fontname='s', color='red')
                screen.draw.text("你的成绩是：" + str(newScore), (350, 420), fontsize=20, fontname='s', color='red')
                txtFile = open('rank', 'w')
                txtFile.write(str(newScore))          #因为打破记录，所以打开rank文件，重新写入新记录
                txtFile.close()
        else:
            screen.draw.text("很遗憾，你没有打破最佳记录：" + str(bestScore), (260, 375), fontsize=20,fontname='s', color='red')
            screen.draw.text("你的成绩是：" + str(newScore), (350, 420), fontsize=20, fontname='s', color='red')

def update():  # 更新模块，每帧重复操作       (上U下D左L右R)
    global  moveDirection
    if keyboard.up:  # 如果按下键盘上键
        moveDirection = 'up'  # 小蛇要向上移
    if keyboard.down:  # 如果按下键盘下键
        moveDirection = 'down'  # 小蛇要向下移
    if keyboard.left:  # 如果按下键盘左键
        moveDirection = 'left'  # 小蛇要向左移
    if keyboard.right:  # 如果按下键盘右键
        moveDirection = 'right'  # 小蛇要向右移

def randintMy(low, high, cutoff):    #用来控制食物产生随机数的，但是产生的随机数不能有在障碍物处
    digit_list = list(range(low, high))
    if type(cutoff) is int:  # 只需要剔除一个值
        if cutoff in digit_list:  # 如果需要剔除的值不存在，则不执行剔除操作
            digit_list.remove(cutoff)
    else:
        for i in cutoff:  # 需要剔除多个值的情况
            if i not in digit_list:  # 如果需要剔除的值不存在，则不执行剔除操作
                continue
            digit_list.remove(i)
    np.random.shuffle(digit_list)
    return digit_list.pop()  # 生成的序列打乱并且返回当前的随机值

def on_mouse_down(pos, button):    #当鼠标按键时执行
    global isRun
    if endButton.collidepoint(pos):  #如果结束键与鼠标位置碰撞
        isRun = False

def move(): # 和蛇相关的一些操作
    global  moveDirection,newScore,isRun,situation
    newSnakeHead = Actor('snake.jpg')
    # 根据moveDirection变量设定新蛇头的坐标，比如小蛇向下移动，就在旧蛇头的下边
    if moveDirection == 'right':  # 小蛇向右移动
        newSnakeHead.x = Snake[0].x + size
        newSnakeHead.y = Snake[0].y
    if moveDirection == 'left':  # 小蛇向左移动
        newSnakeHead.x = Snake[0].x - size
        newSnakeHead.y = Snake[0].y
    if moveDirection == 'up':  # 小蛇向上移动
        newSnakeHead.x = Snake[0].x
        newSnakeHead.y = Snake[0].y - size
    if moveDirection == 'down':  # 小蛇向下移动
        newSnakeHead.x = Snake[0].x
        newSnakeHead.y = Snake[0].y + size

    #游戏失败有三种情况    First.当小蛇（新蛇头）超出边框时游戏失败.   Second.当小蛇蛇头碰到自身时    Third.当小蛇碰到障碍物时
    if newSnakeHead.y < 0 or newSnakeHead.y > HEIGHT \
            or newSnakeHead.x < 0 or newSnakeHead.x > WIDTH:
        isRun = False
        situation = 1
    for i in Snake:                                   #对蛇身进行循环，判断是否和蛇头坐标一致
        if newSnakeHead.x == i.x and newSnakeHead.y == i.y:     #如果蛇头和蛇身坐标一样，不就碰到了
            isRun = False
            situation = 2
            break
    for i in obstacles:                               #对障碍物进行循环，判断是否和蛇头坐标一致
        if newSnakeHead.x == i.x and newSnakeHead.y == i.y:     #如果蛇头和障碍物坐标一样，不就碰到了
            isRun = False
            situation = 3
            break

    # 当小蛇头碰到食物时，不处理，也就是长度+1；饼干重新随机位置出现；
    if newSnakeHead.x == food.x and newSnakeHead.y == food.y:
        #music.play_once('MUSIC')            #你自己加绝对路径  #请换成你自己电脑MUSIC的绝对路径
        food.x = randintMy(1, 40,obstaclesX)*size
        food.y = randintMy(1, 30,obstaclesY)*size
        newScore = newScore + 1 # 得分加1
    else:  # 否则，删除掉旧蛇尾，也就是蛇的长度保持不变
        del Snake[len(Snake)-1]

    Snake.insert(0, newSnakeHead)  # 把新蛇头加到列表的最前面# 当鼠标按键时执行
    if isRun == True:
        clock.schedule_unique(move, 0.15)


move()
pgzrun.go()  # 开始执行游戏