function [List s]=ANPR(directoryname)
5
6	close all;
7	clear all;
8
9	directory=dir('directoryname');
10	s=max(size(directory));
11	List=[];
12
13	for i=3:s;
14	close all;
15	I=imread(directory(i,1).name);
16	[ImgPlate] = LocationPlate(I);
17	[Objects,ImgChar]=Segmentation(ImgPlate);
18	[strPlate] = Recognition(Objects,ImgChar);
19	[r c]=size(strPlate);
20	if c==6
21	strPlate{7}=0;
22	strPlate{8}=0;
23	end
24	if c==7
25	strPlate{8}=0;
26	end
27	List=[List;strPlate];
28	end
29
30	end
