# -*- coding:utf-8 -*-
import arcpy
import random
import os
import glob
import numpy

def random_ClipRaster(trainRaster,labelRaster,outDir,imgNums,imgHeight,imgWidth):   #定义随机裁剪函数（训练原图，标签原图，输出路径，裁剪数量，图像行数，图像列数）
    Min_X = arcpy.GetRasterProperties_management(trainRaster,"LEFT")  #训练原图的X的最小值
    Min_Y = arcpy.GetRasterProperties_management(trainRaster,"BOTTOM") #训练原图的Y的最小值
    Max_X = arcpy.GetRasterProperties_management(trainRaster,"RIGHT") #训练原图的X的最大值
    Max_Y = arcpy.GetRasterProperties_management(trainRaster,"TOP") #训练原图的Y的最大值
    CELLSIZEX = arcpy.GetRasterProperties_management(trainRaster,"CELLSIZEX")  #获取训练原图单像素的宽度
    CELLSIZEY = arcpy.GetRasterProperties_management(trainRaster,"CELLSIZEY") #获取训练原图单像素的高度
    COLUMNCOUNT = arcpy.GetRasterProperties_management(trainRaster,"COLUMNCOUNT") #获取训练原图列数
    ROWCOUNT =arcpy.GetRasterProperties_management(trainRaster,"ROWCOUNT") #获取训练原图行数
    label_Min_X = arcpy.GetRasterProperties_management(labelRaster,"LEFT") #标签原图的X的最小值
    label_Min_Y = arcpy.GetRasterProperties_management(labelRaster,"BOTTOM") #标签原图的Y的最小值
    label_Max_X = arcpy.GetRasterProperties_management(labelRaster,"RIGHT") #标签原图的X的最大值
    label_Max_Y = arcpy.GetRasterProperties_management(labelRaster,"TOP")#标签原图的Y的最大值
    label_CELLSIZEX = arcpy.GetRasterProperties_management(labelRaster,"CELLSIZEX")  #获取标签原图单像素的宽度
    label_CELLSIZEY = arcpy.GetRasterProperties_management(labelRaster,"CELLSIZEY") #获取标签原图单像素的高度
    label_COLUMNCOUNT = arcpy.GetRasterProperties_management(labelRaster,"COLUMNCOUNT") #获取标签原图列数
    label_ROWCOUNT =arcpy.GetRasterProperties_management(labelRaster,"ROWCOUNT") #获取标签原图行数
    rotate_list = ["90","180","270","mirror"]
    mkdir_dem = outDir + "train_dem"  
    mkdir_label = outDir + "train_label"
    os.popen("mkdir "+mkdir_dem) #计算机先自动生成文件夹
    os.popen("mkdir "+mkdir_label)
    if (str(label_Min_X) == str(Min_X)) and (str(label_Min_Y) == str(Min_Y))and ( str(Max_X) == str(label_Max_X))and( str(Max_Y) == str(label_Max_Y))and (str(label_CELLSIZEX) == str(CELLSIZEX))and(str(label_CELLSIZEY)== str(CELLSIZEY))and( str(COLUMNCOUNT) == str(label_COLUMNCOUNT))and(str(ROWCOUNT)== str(label_ROWCOUNT)):
        num =0
        #print("test")
        while num < imgNums:
            random_x = random.randint(0,int(str(COLUMNCOUNT)) - imgWidth) #拟随机生成行列号来生成图像，(0,COLUMNCOUNT - imgWidth)为可选列号的范围
            random_y = random.randint(0,int(str(ROWCOUNT))- imgHeight) #(0,ROWCOUNT- imgHeight)为可选行号的范围
            temp_x = float(str(Min_X)) + random_x * float(str(CELLSIZEX)) #temp_x为所选图像左下角的横坐标
            temp_y = float(str(Min_Y))  + random_y * float(str(CELLSIZEY)) #temp_y为所选图像左下角的纵坐标
            cood_xy = str(temp_x) + " " +str(temp_y) + " " +str(temp_x + imgWidth*(float(str(CELLSIZEX)))) + " " + str(temp_y + imgHeight*(float(str(CELLSIZEY))))#所选图像的左下坐标和右上坐标
            #print(cood_xy)
            out_demRaster = outDir+"train_dem\\"+"dem"+"_"+ str(num) + ".tif"#dem_1.tif  dem_2.tif
            out_labelRaster = outDir+"train_label\\" +"label" +"_" +str(num) +".tif" #label_1.tif  label_2.tif
            arcpy.Clip_management(trainRaster,cood_xy,out_demRaster,"#","#","NONE","MAINTAIN_EXTENT") #裁剪输出
            arcpy.Clip_management(labelRaster,cood_xy,out_labelRaster,"#","#","NONE","MAINTAIN_EXTENT") #裁剪输出
            #arcpy.Clip_management(trainRaster,cood_xy,out_demRaster,"#","#","NONE","NO_MAINTAIN_EXTENT") #裁剪输出
            #arcpy.Clip_management(labelRaster,cood_xy,out_labelRaster,"#","#","NONE","NO_MAINTAIN_EXTENT") #裁剪输出
            dem_numpy = arcpy.RasterToNumPyArray(out_demRaster,nodata_to_value=-9999) #栅格转成numpy,目的是统一设置nodata值为-9999，用于后面的判断
            dem_numpy = numpy.hstack(dem_numpy) #把numpy数组元素变成一维，用于方便循环
            for value in list(dem_numpy):
                if value == -9999:
                    noDataValue = -9999
                    break
                else :
                    noDataValue = "None"
            if noDataValue == "None":
                random_rotate = random.randint(0,3)
                out_demRotateRaster =  outDir+"train_dem\\"+"dem"+"_"+ str(num) +"_"+rotate_list[random_rotate]+ ".tif"  #dem_1.tif  dem_2.tif
                out_labelRotateRaster =  outDir+"train_label\\"+"label"+"_"+ str(num) +"_"+rotate_list[random_rotate]+ ".tif" #dem_1.tif  dem_2.tif
                if rotate_list[random_rotate] == "mirror":
                    arcpy.Mirror_management(out_demRaster,out_demRotateRaster) #镜像操作
                    arcpy.Mirror_management(out_labelRaster,out_labelRotateRaster)
                else :
                    rotate_x = temp_x + (imgWidth*float(str(CELLSIZEX)))/2   #计算旋转中心
                    rotate_y = temp_y + (imgHeight*float(str(CELLSIZEY)))/2
                    arcpy.Rotate_management(out_demRaster,out_demRotateRaster,rotate_list[random_rotate],str(rotate_x)+" "+str(rotate_y))  #旋转操作
                    arcpy.Rotate_management(out_labelRaster,out_labelRotateRaster,rotate_list[random_rotate],str(rotate_x)+" "+str(rotate_y))

                print("%dth and conversion %s images are generated"%(num,rotate_list[random_rotate])) #提示图片裁剪好了
                num = num+1 #图片保留，继续循环
            else:  #删除生成的train和label图片
                remove_dem = glob.glob(outDir + "train_dem\\" + "dem" + "_" + str(num) + ".*")  #每一个图片有好几个文件，都需要删除
                remove_label = glob.glob(outDir + "train_label\\" + "label" + "_" + str(num) + ".*")
                for tiff in remove_dem:
                    #print(tiff)
                    os.remove(tiff)
                    print("Delete"+ " " + tiff)
                for label_tiff in remove_label:
                    os.remove(label_tiff)
                    print("Delete"+ " " + label_tiff)
                num = num
    else :
        Error = " Image matching failed "  #两张源图片格式如果大小不匹配，无法运用此函数，直接error
        print(Error)
        return
    print("Successfully Done!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


print("Start!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
trainRaster = "G:\\Graduation_thesis\\DATA\\pointcloud\\xining\\xining_dsm.tif"
labelRaster = "G:\\Graduation_thesis\\DATA\\pointcloud\\xining\\xining_label.tif"
outDir = "G:\\test_env\\"
imgNums = 5
imgHeight = 256
imgWidth = 256
random_ClipRaster(trainRaster,labelRaster,outDir,imgNums,imgHeight,imgWidth)
