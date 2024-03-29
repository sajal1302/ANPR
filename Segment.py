function [Objects,ImgChar]=Segmentation(ImgPlate)
5
6	%% Binarize the image %%
7
8	level = graythresh(ImgPlate);
9	Ibw =(im2bw(ImgPlate,level));
10
11	%% Select the orientation of the largest object in the image.
12	%% Turn this angle at the picture.
13	%% Plate cutting to segment the characters that compose %%
14
15	Fl=bwlabel(Ibw);
16	Statsbf=regionprops(Fl,'all');
17	Flmax=find([Statsbf.Area]==max([Statsbf.Area]));
18	angle=Statsbf(Flmax).Orientation;
19	F2=imrotate(Fl,-angle);
20
 


21	L=bwlabel(F2);
22	Statsbf=regionprops(L,'all');
23	maxi=find([Statsbf.Area]==max([Statsbf.Area]));
24	BB=Statsbf(maxi).BoundingBox;
25	F2=imcrop(F2,[BB(1,1) BB(1,2) BB(1,3) BB(1,4)]);
26
27	%% First three and last three rows to zero.
28	%% First two and last two columns to zero.
29	%% So remove connectivity between characters and background %%
30	%% Remove small impurities %%
31
32	L4=not(F2);
33	[r c]=size(L4);
34	L4(1,:)=0;
35	L4(2,:)=0;
36	L4(3,:)=0;
37	L4(r,:)=0;
38	L4(r-1,:)=0;
39	L4(r-2,:)=0;
40	L4(:,1)=0;
41	L4(:,2)=0;
42	L4(:,c)=0;
43	L4(:,c-1)=0;
44
45	L4b=bwlabel(L4);
46	Stats3=regionprops(L4b,'all');
47	sarea3=[Stats3.Area];
48	G=find(sarea3<70);
49
50	for cv=1:length(G)
51	G1=find(L4b==G(cv));
52	L4(G1)=0;
53	end
54	[r c]=size(L4);
55	CC=bwconncomp(L4);
56	L=bwlabel(L4);
57	ind2=max(L(:,c-2));
58	P=regionprops(CC,'all');
59
60	%% Remove objects smaller and larger than a character %%
61
62	i=1;
63	if	(max(P(i,1).PixelList(:,1))-min(P(i,1).PixelList(:,1)))<(c/13)
64	L4(CC.PixelIdxList{1,i})=0;
65	end
66
67	for i=1:CC.NumObjects
68
69	if (max(P(i,1).PixelList(:,1))-min(P(i,1).PixelList(:,1)))>(2*c/3)
70	L4(CC.PixelIdxList{1,i})=0;
71	end
72
73	if (max(P(i,1).PixelList(:,2))-min(P(i,1).PixelList(:,2)))<(r/3)
 



74	L4(CC.PixelIdxList{1,i})=0;
75	end
76	
77	if (max(P(i,1).PixelList(:,1))-min(P(i,1).PixelList(:,1)))<(c/8)
78	L4(find(L==ind2))=0;
79	end
80	
81	end
82	
83	L4=imclose(L4,strel('disk',1));
84	L4=imopen(L4,strel('disk',1));
85	figure(4);
86	imshow(L4);
87	L4b=bwlabel(L4);
88	Stats3b=regionprops(L4b,'all');
89	
90	N=length(Stats3b);
91	
92	while N>8
93	L4=imdilate(L4,strel('disk',1));
94	L4b=bwlabel(L4);
95	Stats3b=regionprops(L4b,'all');
96	N=length(Stats3b);
97	end
98	
99	L4b=bwlabel(L4);
100	Stats3b=regionprops(L4b,'all');
101	ImgChar=zeros(100,100,N);
102	
103	%% Dividing characters which are connected %%
104	%% Remove objects that have been listed as characters but are not%
105	%% Show every character in the correct position %%
106	
107	cont=0;
108	cont1=0;
109	
110	for i=1:N
111	
112	[r1 c1]=size(Stats3b(i,1).Image);
113	
114	if c1>round(c/6)
115	cont1=cont;
116	Stats3b(i,1).Image(:,round(c1/2))=0;
117	L5=Stats3b(i,1).Image;
118	CC=bwconncomp(L5);
119	CC1=regionprops(CC,'all');
120	
121	for j=1:CC.NumObjects
122	[r2 c2]=size(CC1(j,1).Image);
123	
124	if c2>round(c/7)
125	CC1(j,1).Image(:,round(c2/2))=0;
126	L6=CC1(j,1).Image;
 



127		LL=bwconncomp(L6);
128		CC2=regionprops(LL,'all');
129		
130		for k=1:LL.NumObjects
131		CC2(k).Image=imresize(CC2(k).Image, [100 100]);
132		figure;imshow((CC2(k).Image))
133		ImgChar(:,:,i+cont1)=not(CC2(k).Image);
134		cont1=cont1+1;
135		end
136		cont=cont+1;
137		
138		else
139		
140		CC1(j).Image=imresize(CC1(j).Image, [100 100]);
141		figure;imshow((CC1(j).Image))
142		ImgChar(:,:,i+cont1)=not(CC1(j).Image);
143		cont1=cont1+1;
144		end
145		
146		end
147		cont=cont+1;
148		
149		else
150		Stats3b(i).Image=imresize(Stats3b(i).Image, [100 100]);
151		figure;imshow((Stats3b(i).Image));
152		
153		if cont~=0
154		ImgChar(:,:,i+cont)=not(Stats3b(i).Image);
155		else
156		ImgChar(:,:,i)=not(Stats3b(i).Image);
157		end
158		end
159	End	
160		
161	%%	Remove spurious %%
162		
163	[x	y Objects]=size(ImgChar);
164		
165		for p=1:Objects
166		
167		if min(min(not(ImgChar(:,:,p))))==1;
168		l=p;
169		while l~=(Objects-1)
170		ImgChar(:,:,l)=ImgChar(:,:,l+1);
171		l=l+1;
172		end
173		ImgChar(:,:,l)=ImgChar(:,:,l+1);
174		Objects=Objects-1;
175		end
176		end
177	end	
