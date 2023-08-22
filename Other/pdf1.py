from PIL import Image
import matplotlib.pyplot as plt
import os
import time
import fitz
import pandas as pd
#from pdf2image import convert_from_path
#from wand.image import *
lso=[]
folder=r"\\jpgtkopjl2vwsfs.code1.emi.philips.com\Tokyo\CFCSCM_OM"
# def get_pixmaps_in_pdf(pdf_filename):
#     doc = fitz.open(pdf_filename)
#     xrefs = set()
#     for page_index in range(doc.pageCount):
#         for image in doc.getPageImageList(page_index):
#             xrefs.add(image[0])  # Add XREFs to set so duplicates are ignored
#     pixmaps = [fitz.Pixmap(doc, xref) for xref in xrefs]
#     doc.close()
#     return pixmaps


# def write_pixmaps_to_pngs(pixmaps):
#     for i, pixmap in enumerate(pixmaps):
#         if i==0:
#             pixmap.writePNG(f'{i}.png')  # Might want to come up with a better name




def checkpdf(so,dt,ENAME):
    #print(so,dt)
    files=os.listdir(folder)
    find=0
    for pdf in files:
        #print(pdf)
        if pdf.find(so)>-1:
            find=1
            doc = fitz.open(folder+"\\"+pdf)
            #doc = fitz.open(r"C:\Users\320144297\Downloads\6600590555&6600590556&6600591151.pdf")
            n=0
            all=len(doc)
            #print(all)
            print(f"这票检收是：SO：{so},检收日：{dt},医院：{ENAME}")
            for i in range( all):
                page=doc.load_page(i) # 获取第0页
                trans=fitz.Matrix(2,2)#.prerotate()
                pix = page.get_pixmap(matrix=trans,alpha=False)#  get_pixmap()
                pix.save( str(i) + ".jpg")
                img_now2 = Image.open( str(i) +".jpg" )
                plt.imshow( img_now2)
                plt.show()
                plt.close()

            # image_pdf = Image(filename=folder+"\\"+pdf) #,resolution=300
            # image_jpeg = image_pdf.convert('jpg')
            # image_jpeg.save("0.jpg")
            
            # img_now = Image.open( "0.jpg" )
            # #split_area = ( 100, 600, 600, 800)
            # #split_area = ( 200, 1200, 1200, 1600)
            # split_area = ( 700, 400, 1200,600)
            # img_now.crop(split_area).save("1.jpg")
            # split_area2 =  ( 200, 1200, 1200, 1600)
            # img_now.crop(split_area2).save("2.jpg")
            # #time.sleep(0.5) 
            # img_now = Image.open( "1.jpg" )
            
            # plt.imshow(img_now)
            # print(f"这票检收是：SO：{so},检收日：{dt}")
            # plt.show()
            #time.sleep(2) 
            #plt.close()
            #img_now2 = Image.open( "0.jpg" )
            #plt.imshow(img_now)
            #plt.imshow( img_now2)
            #print(f"这票检收是：SO：{so},检收日：{dt},YI{ENAME}")
            #plt.show()
            #plt.close()
            doc=""
            os.rename( folder+"\\"+pdf, r"\\jpgtkopjl2vwsfs.code1.emi.philips.com\Tokyo\CFCSCM_OM\共有データ\売上処理_2022\back"+"\\"+pdf)



            ck=input(f"这票检收是：SO：{so},检收日：{dt},YI{ENAME}不对按'N',否则按回车确认")
            if ck=="N" or ck=="n":
                #print(f"{so}的检收日不对，要看一下。")
                 

                lso.append(f"{so}\t{pdf}\tNG")
            else:
                lso.append(f"{so}\t{pdf}\tOK")

    if find==0:
        print(f"{so}找不到检收书。")

if __name__=='__main__':
    
    # pixmaps = get_pixmaps_in_pdf(r'\\jpgtkopjl2vwsfs.code1.emi.philips.com\Tokyo\CFCSCM_OM\GBS Training\00_売上処理用 検収書\MATC\6600582803.pdf')
    # write_pixmaps_to_pngs(pixmaps)
    #checkpdf('1', '1','1')

    xlsfile = r"C:\Users\320126252\Desktop\Book1.xlsx"
    data = pd.read_excel(xlsfile,header=0)
    data1=data[["SO","Billing date","Bill to Name"]]
    data2=data1.drop_duplicates().dropna()
    for index,row in data2.iterrows():
        checkpdf(str(int(row['SO'])), row['Billing date'],row['Bill to Name'])
    for x in lso:
        print(x)










# #这里是设置参数的
# #图片文件路径
# img_path = 'imgTest.jpg'
# #分割成几行
# img_split_row = 5
# #分割成几列
# img_split_col = 5


# #接下来开始运行程序
# #要保存的图片路径(保存为png图片格式)
# if os.path.dirname(img_path) == "" :
#     img_path = os.getcwd()+"//"+img_path
# img_save = os.path.dirname(img_path)+"//图片分割-"+os.path.splitext(os.path.basename(img_path))[0]+"//"
# if not os.path.exists(img_save):
#     os.makedirs(img_save)
# #分割图片
# img_ext_name = os.path.splitext(os.path.basename(img_path))[1]
# img_now = Image.open( img_path )
# split_size_w = int( img_now.size[0]/img_split_col )
# split_size_h = int( img_now.size[1]/img_split_row )
# for r in range(img_split_row):
#     for c in range(img_split_col):
#         split_area = ( split_size_w*c, r*split_size_h, split_size_w*(c+1), split_size_h*(r+1) )
#         print( (r*img_split_col+c+1) );
#         img_now.crop(split_area).save(img_save+str(r*img_split_col+c+1)+img_ext_name)
#         time.sleep(0.5) #等待
# #结束
# print("图片分割结束，一共"+str(img_split_row*img_split_col)+"张图片（保存在"+img_save)


