import cv2 as cv
import numpy as np
import math
feed=cv.VideoCapture(1)
while True:
	ret,frame=feed.read()
	ROWS,COLUMNS=frame.shape[0],frame.shape[1]
	x_max,y_max=ROWS-1,COLUMNS-1
	p=(COLUMNS/2,ROWS/2)
	gry=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	ta,img=cv.threshold(gry,100,255,cv.THRESH_BINARY)
	kernel=cv.getStructuringElement(cv.MORPH_RECT,(15,15))
	img=cv.morphologyEx(img,cv.MORPH_OPEN,kernel)
	img=cv.morphologyEx(img,cv.MORPH_CLOSE,kernel)
	im2, con, hi= cv.findContours(img,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
	for i in range(len(con)):
		arcl=cv.arcLength(con[i],True)
		if arcl>1000:
			error_thresh=37
			contour=cv.approxPolyDP(con[i],error_thresh,True)
			n=len(contour)
	if n==4:
		aa,ab=abs(contour[1][0][0]-contour[0][0][0]),abs(contour[1][0][1]-contour[0][0][1])
		ba,bb=abs(contour[2][0][0]-contour[1][0][0]),abs(contour[2][0][1]-contour[1][0][1])
		u=max(aa,ab)
		v=max(ba,bb)
		if u<v:
			p1=((contour[1][0][0]+contour[0][0][0])/2,(contour[1][0][1]+contour[0][0][1])/2)
			p2=((contour[2][0][0]+contour[3][0][0])/2,(contour[2][0][1]+contour[3][0][1])/2)
		else:
			p1=((contour[1][0][0]+contour[2][0][0])/2,(contour[1][0][1]+contour[2][0][1])/2)
			p2=((contour[0][0][0]+contour[3][0][0])/2,(contour[0][0][1]+contour[3][0][1])/2)
		C_LINE=np.array([[[p1[0],p1[1]]],[[p2[0],p2[1]]]],dtype=np.int32)
		REF_LINE=C_LINE
		if (abs(REF_LINE[0][0][1]-REF_LINE[1][0][1])>x_max-15):
			xv=(REF_LINE[0][0][0]+REF_LINE[1][0][0])/2
			if (xv>p[0]):
				LoR_Factor=1
			else:
				LoR_Factor=-1
		elif (abs(REF_LINE[0][0][0]-REF_LINE[1][0][0])>y_max-15):
			yh=(REF_LINE[0][0][1]+REF_LINE[1][0][1])/2
			if (yh>p[1]):
				LoR_Factor=1
			else:
				LoR_Factor=-1
	elif n==6:
		p1x=0
		p2y=0
		for i in contour:
			if (i[0][0]==0 or i[0][0]==y_max):
				p2y+=i[0][1]/2
				qwe=i[0][0]
			if (i[0][1]==0 or i[0][1]==x_max):
				p1x+=i[0][0]/2
				qws=i[0][1]
		p1=(p1x,qws)
		p2=(qwe,p2y)
		S_LINE=np.array([[[p1x,qwe]],[[qws,p2y]]],dtype=np.int32)
		REF_LINE=S_LINE
	elif (n==12 or n==8):
		break
	DIST_OUT=cv.pointPolygonTest(REF_LINE,p,True)
	img=cv.line(img,p1,p2,(100,100,100),5)
	cv.imshow('BRO',img)
	cv.waitKey(1)
	print "DISTANCE: ",LoR_Factor*DIST_OUT
feed.release()