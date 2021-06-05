function [ImgPlate] = LocationPlate(I)
5
6 %% Cutting and resizing the original image %%
7
8	[rows columns]=size(I);
9	columns=columns/3;
10	xmin=round(0.20*rows);
11	ymin=round(0.20*columns);
12	width=round((0.85*columns)-(0.10*columns));
13	height=round((0.85*rows)-(0.15*rows)); 14 Io=imcrop(I,[xmin ymin width height]); 15 Io=imresize(Io,[480 640]);
16	Io=rgb2gray(Io);
17	Io=imadjust(Io);
18
19	%% Image processing to focus the area of number plate %%
20	%% Smooth edges and contours to delete characters.
21	%% Subtracting the original image to obtain the information
22	%% previously deleted and thus stay with the characters.
23	%% Select the elements with a higher level of 85.
24	%% Pass a mask to the image to remove excess information common to
25	%% all images.
26
27	se=strel('rectangle',[6 30]);
28	Ic=imclose(Io,se);
29	Ic=imadjust(Ic);
30	tophat=Ic-Io;
31	Ibw1=(tophat>85);
32	Ibw=Ibw1 & im2bw(imread('marco.bmp'));
33
34	%% Remove the related elements with fewer than 70 pixels %%
35	%% Remove objects that are not plate %%
36
37	plate= bwlabel(Ibw,4);
38	obj= max(max(plate));
39	dim1 = regionprops(plate, 'area')';
40	dim=[dim1.Area];
41	dim(find(dim<70))=0;
42
43 for i=1:obj
44
45	index=find(plate==i);
46	if dim(i)==0
47	plate(index)=0;
48	else
49	plate(index)=1;
50	end
51
52 end
53
54	CC=bwconncomp(plate);
55	P=regionprops(CC,'all');
56	[rp cp]=size(plate);
 


57	for i=1:CC.NumObjects
58
59	if P(i).MajorAxisLength>(2*cp/3)
60	plate(P(i).PixelIdxList(:,1))=0;
61	end
62
63 end
64
65 %% Remove objects that are not candidates for plate %%
66
67	se3=strel('rectangle',[30 70]);
68	r2=imclose(plate,se3);
69
70	se2=strel('rectangle',[5 30]);
71	r=imdilate(r2,se2);
72
73	CC=bwconncomp(r);
74	P=regionprops(CC,'all');
75
76 for i=1:CC.NumObjects
77
78	if P(i).MajorAxisLength>(2*cp/3)
79	r(P(i).PixelIdxList(:,1))=0;
80	end
81
82 end
83
84	%% select the largest connected component after preprocessing, the
85	%%plate
86
87	plate1= bwlabel(r,4);
88	dim2= regionprops(plate1, 'area')';
89	dim1=[dim2.Area];
90	f=max(dim1);
91	indMax=find(dim1==f);
92	plate1(find(plate1~=indMax))=0;
93
94 %% cutting of original image %%
95
96	[cuty, cutx] = find( plate1 > 0);
97	up = min(cuty);
98	down = max(cuty);
99	left = min(cutx);
100	right = max(cutx);
101	
102	img_cut_v = Io(up:down,:,:);
103	img_cut_h = img_cut_v(:,left:right,:);
104	
105	ImgPlate = img_cut_h;
106	
107	%% different mask for location plate %%
108	
109	[r c]=size(ImgPlate);
 



110	if	r<25 || r>65
111		
112		[rows columns]=size(I);
113		columns=columns/3;
114		xmin=round(0.20*rows);
115		ymin=round(0.20*columns);
116		width=round((0.85*columns)-(0.10*columns));
117		height=round((0.85*rows)-(0.15*rows));
118		Io=imcrop(I,[xmin ymin width height]);
119		Io=imresize(Io,[480 640]);
120		Io=rgb2gray(Io);
121		Io=imadjust(Io);
122		
123		se=strel('rectangle',[6 30]);
124		Ic=imclose(Io,se);
125		Ic=imadjust(Ic);
126		tophat=Ic-Io;
127		Ibw1=(tophat>85);
128		mask=zeros(480,640);
129		
130		for i=40:370
131		for j=40:575
132		mask(i,j)=1;
133		end
134		end
135		
136		Ibw=Ibw1 & im2bw(mask);
137		plate= bwlabel(Ibw,4);
138		obj= max(max(plate));
139		dim1 = regionprops(plate, 'area')';
140		dim=[dim1.Area];
141		dim(find(dim<70))=0;
142		
143		for i=1:obj
144		index=find(plate==i);
145		if dim(i)==0
146		plate(index)=0;
147		else
148		plate(index)=1;
149		end
150		end
151		
152		CC=bwconncomp(plate);
153		P=regionprops(CC,'all');
154		[rp cp]=size(plate);
155		
156		for i=1:CC.NumObjects
157		if P(i).MajorAxisLength>(cp/3)
158		plate(P(i).PixelIdxList(:,1))=0;
159		end
160		end
161		
162		se3=strel('rectangle',[30 70]);
 



163		r2=imclose(plate,se3);
164		se2=strel('rectangle',[5 30]);
165		r=imdilate(r2,se2);
166		
167		plate1= bwlabel(r,4);
168		dim2= regionprops(plate1, 'area')';
169		dim1=[dim2.Area];
170		f=max(dim1);
171		indMax=find(dim1==f);
172		plate1(find(plate1~=indMax))=0;
173		
174		[cuty, cutx] = find( plate1 > 0);
175		up = min(cuty);
176		down = max(cuty);
177		left = min(cutx);
178		right = max(cutx);
179		img_cut_v = Io(up:down,:,:);
180		img_cut_h = img_cut_v(:,left:right,:);
181		ImgPlate = img_cut_h;
182		
183	end	
184		
185	%% Representation %%
186
187	% figure(1);
188	% imshow(I);
189	% subplot(2,2,1);imshow(I);
190	% subplot(2,2,2);imshow(Ic);
191	% subplot(2,2,3);imshow(plate);
192	% subplot(2,2,4);imshow(plate1);
193	
194	figure(2);
195	imshow(img_cut_h);title('output location plate');
196	
197	end
