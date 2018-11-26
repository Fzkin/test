#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 16:45:53 2018

@author: fzlin
"""



import wx
import cv2

COVER = 'camera.png' 
class MyFrame(wx.Frame): 
    def __init__(self,parent, id, title): 
        wx.Frame.__init__(self, parent, id, title, size=(600,600)) 
        self.panel = wx.Panel(self)
        self.Center()
        
         # 封面图片
        self.image_cover = wx.Image(COVER, wx.BITMAP_TYPE_ANY).Scale(350,300)
        # 显示图片在panel上
        self.bmp = wx.StaticBitmap(self.panel, -1, wx.Bitmap(self.image_cover))
        start_button = wx.Button(self.panel,label='Start')
        close_button = wx.Button(self.panel,label='Close')

        self.Bind(wx.EVT_BUTTON,self._learning_face,start_button)
        self.Bind(wx.EVT_BUTTON,self.close_face,close_button)
        # 基于GridBagSizer的界面布局
        # 先实例一个对象
        self.grid_bag_sizer = wx.GridBagSizer(hgap=5,vgap=5)
        # 注意pos里面是先纵坐标后横坐标
        self.grid_bag_sizer.Add(self.bmp, pos=(0, 0), flag=wx.ALL | wx.EXPAND, span=(4, 4), border=5)
        self.grid_bag_sizer.Add(start_button, pos=(4, 1), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, span=(1, 1), border=5)
        self.grid_bag_sizer.Add(close_button, pos=(4, 2), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, span=(1, 1), border=5)

        self.grid_bag_sizer.AddGrowableCol(0,1)
        #grid_bag_sizer.AddGrowableCol(0,2)

        self.grid_bag_sizer.AddGrowableRow(0,1)
        #grid_bag_sizer.AddGrowableRow(0,2)

        self.panel.SetSizer(self.grid_bag_sizer)
        # 界面自动调整窗口适应内容
        self.grid_bag_sizer.Fit(self)
        '''
        sizer = wx.GridBagSizer(6, 6)
        sizer.Add(wx.Button(self, -1, "监控_按钮1"), (0, 0), (3, 2), wx.EXPAND) 
        sizer.Add(wx.Button(self, -1, "监控_按钮2"), (0, 2), (3, 2), wx.EXPAND) 
        sizer.Add(wx.Button(self, -1, "监控_按钮3"), (3, 0), (3, 2), wx.EXPAND) 
        sizer.Add(wx.Button(self, -1, "监控_按钮4"), (3, 2), (3, 2), wx.EXPAND) 
        sizer.Add(wx.Button(self, -1, "开启_按钮5"), (0, 4), (1, 1), wx.ALIGN_CENTER) 
        sizer.Add(wx.Button(self, -1, "关闭_按钮6"), (0, 5), (1, 1), wx.ALIGN_CENTER)
        sizer.Add(wx.Button(self, -1, "搜索_按钮7"), (2, 5), (1, 1), wx.ALIGN_CENTER)
        sizer.Add(wx.Button(self, -1, "显示扫描信息_按钮8"), (3, 4), (3, 2), wx.EXPAND)
        sizer.Add(wx.TextCtrl(self, -1, "文本框_按钮9"), (2, 4), (1, 1), wx.EXPAND)
        sizer.Add(wx.Button(self, -1, "未离校名单_按钮10"), (1, 5), (1, 1), wx.ALIGN_CENTER)
        sizer.Add(wx.Button(self, -1, "未入校名单_按钮10"), (1, 4), (1, 1), wx.ALIGN_CENTER)
        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(3)
        sizer.AddGrowableCol(0,3)
        sizer.AddGrowableCol(2,3)
        sizer.AddGrowableCol(4)
        sizer.AddGrowableCol(5)
        self.SetSizerAndFit(sizer) 
        self.Centre()
        '''
    
    def _learning_face(self,event):
        #建cv2摄像头对象，这里使用电脑自带摄像头，如果接了外部摄像头，则自动切换到外部摄像头
        self.cap = cv2.VideoCapture(1)
        # 设置视频参数，propId设置的视频参数，value设置的参数值
        self.cap.set(3, 480)
        # 截图screenshoot的计数器
        self.cnt = 0

        # cap.isOpened（） 返回true/false 检查初始化是否成功
        while(self.cap.isOpened()):

            # cap.read()
            # 返回两个值：
            #    一个布尔值true/false，用来判断读取视频是否成功/是否到视频末尾
            #    图像对象，图像的三维矩阵
            flag, im_rd = self.cap.read()
            # 每帧数据延时1ms，延时为0读取的是静态帧
            self.k = cv2.waitKey(1)

            # 待会要显示在屏幕上的字体
            font = cv2.FONT_HERSHEY_SIMPLEX
            # 添加说明
            cv2.putText(im_rd, "S: screenshot", (20, 400), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.putText(im_rd, "Q: quit", (20, 450), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            # 按下s键截图保存
            if (self.k == ord('s')):
                self.cnt += 1
                cv2.imwrite("screenshoot"+str(self.cnt)+".jpg", im_rd)

            # 按下q键退出
            if(self.k == ord('q')):
                break

            # 使用opencv会在新的窗口中显示
            # cv2.imshow("camera", im_rd)

            # 现将opencv截取的一帧图片BGR转换为RGB，然后将图片显示在UI的框架中
            height,width = im_rd.shape[:2]
            image1 = cv2.cvtColor(im_rd, cv2.COLOR_BGR2RGB)
            pic = wx.Bitmap.FromBuffer(width,height,image1)
            # 显示图片在panel上
            self.bmp.SetBitmap(pic)
            self.grid_bag_sizer.Fit(self)

        # 释放摄像头
        self.cap.release()
        # 删除建立的窗口
        # cv2.destroyAllWindows()


    
    
    def learning_face(self,event):
        """使用多线程，子线程运行后台的程序，主线程更新前台的UI，这样不会互相影响"""
        import threading
        # 创建子线程，按钮调用这个方法，
        t = threading.Thread(target=self._learning_face, args=(event,))
        t.start()        


    def close_face(self,event):
        """关闭摄像头，显示封面页"""
        self.cap.release()
        self.bmp.SetBitmap(wx.Bitmap(self.image_cover))
        self.grid_bag_sizer.Fit(self)
class MyApp(wx.App): 
    def OnInit(self): 
        frame = MyFrame(None, -1, 'wxgridbagsizer.py') 
        frame.Show(True) 
        return True 
app = MyApp(0) 
app.MainLoop()