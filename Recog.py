function [strPlate] = Recognition(Objects,ImgChar)
5
6	%% Load databases numbers and letters for comparison %%
7
8	Baseletters=im2bw(uint8(imread('Letras.jpg')));
9	Baseletters=bwlabel(Baseletters);
10	L=regionprops(Baseletters,'all');
11
12	letters={'A','N','B','O','P','C','Q','D','R','E','S','F','T','G','
U','H','V','I','J','W','K','X','L','Y','M','Z'};
13
14	letters1={'A','N','B','O','P','C','O','D','R','E','S','F','T','O',
'U','H','V','I','J','W','K','X','L','Y','M','Z'};
15
16	for i=1:26
17	L(i).Image=imresize(L(i).Image,[100 100]);
18	end
19
20	N=struct('Image',{});
21	numbers={'0','1','2','3','4','5','6','7','8','9'};
22
23	N(1).Image=imresize(im2bw(uint8(imread('0.png'))),[100 100]);
24	N(2).Image=imresize(im2bw(uint8(imread('1.png'))),[100 100]);
25	N(3).Image=imresize(im2bw(uint8(imread('2.png'))),[100 100]);
26	N(4).Image=imresize(im2bw(uint8(imread('3.png'))),[100 100]);
27	N(5).Image=imresize(im2bw(uint8(imread('4.png'))),[100 100]);
28	N(6).Image=imresize(im2bw(uint8(imread('5.png'))),[100 100]);
29	N(7).Image=imresize(im2bw(uint8(imread('6.png'))),[100 100]);
30	N(8).Image=imresize(im2bw(uint8(imread('7.png'))),[100 100]);
31	N(9).Image=imresize(im2bw(uint8(imread('8.png'))),[100 100]);
32	N(10).Image=imresize(im2bw(uint8(imread('9.png'))),[100 100]);
33
34	%% Treat the image depending on the number of objects found %%
35
36	I=ImgChar;
37
38	%% Maximum of objects is 8, if more, you must remove the leftover%
39
40	if (Objects>8)
41
42	for i=1:Objects
43	char=I(:,:,i);
44	char=not(uint8(char));
45	list_corr=[];
46	for j=1:26
47	corr=corr2(L(j).Image,char);
48	list_corr=[list_corr corr];
49	end
50	for j=1:10
51	corr=corr2(N(j).Image,char);
52	list_corr=[list_corr corr];
53	end
54	f=max(list_corr);
 


55	if f<0.3
56	ImgChar(:,:,i)=0;
57	end
58	end
59
60	for p=1:Objects
61	if min(min(not(ImgChar(:,:,p))))==1;
62	for l=p:(Objects-1)
63	ImgChar(:,:,l)=ImgChar(:,:,l+1);
64	end
65	ImgChar(:,:,l)=ImgChar(:,:,l+1);
66	Objects=Objects-1;
67	end
68	end
69	end
70
71	%% Distinguish between 6, 7 or 8 objects for correlation %%
72
73	if Objects==6
74
75	strPlate=[];
76	for i=1:Objects
77	char=ImgChar(:,:,i);
78	char=not(uint8(char));
79
80	if (i==1) || (i==6)
81	list_corr=[];
82	for j=1:26
83	corr=corr2(L(j).Image,char);
84	list_corr=[list_corr corr];
85	end
86	f=max(list_corr);
87	maxcorr=find(list_corr==f);
88	strPlate=[strPlate letters(maxcorr)];
89	end
90
91	if (i==2) || (i==3) || (i==4) || (i==5)
92	list_corr=[];
93	for j=1:10
94	corr=corr2(N(j).Image,char);
95	list_corr=[list_corr corr];
96	end
97	f=max(list_corr);
98	maxcorr=find(list_corr==f);
99	strPlate=[strPlate numbers(maxcorr)];
100	end
101	end
102	end
103	
104	if Objects==8
105	
106	strPlate=[];
107	for i=1:Objects
 


108	char=ImgChar(:,:,i);
109	char=not(uint8(char));
110	
111	if (i==1) || (i==7) || (i==8)
112	list_corr=[];
113	for j=1:26
114	corr=corr2(L(j).Image,char);
115	list_corr=[list_corr corr];
116	end
117	f=max(list_corr);
118	maxcorr=find(list_corr==f);
119	strPlate=[strPlate letters(maxcorr)];
120	end
121	
122	if (i==2)
123	list_corr=[];
124	for j=1:26
125	corr=corr2(L(j).Image,char);
126	list_corr=[list_corr corr];
127	end
128	f=max(list_corr);
129	maxcorr=find(list_corr==f);
130	strPlate=[strPlate letters1(maxcorr)];
131	end
132	
133	if (i==3) || (i==4) || (i==5) || (i==6)
134	list_corr=[];
135	for j=1:10
136	corr=corr2(N(j).Image,char);
137	list_corr=[list_corr corr];
138	end
139	f=max(list_corr);
140	maxcorr=find(list_corr==f);
141	strPlate=[strPlate numbers(maxcorr)];
142	end
143	end
144	end
145	
146	if	Objects==7
147		
148		strPlate=[];
149		for i=1:Objects
150		char=ImgChar(:,:,i);
151		char=not(uint8(char));
152		
153		if (i==1) || (i==7)
154		list_corr=[];
155		for j=1:26
156		corr=corr2(L(j).Image,char);
157		list_corr=[list_corr corr];
158		end
159		f=max(list_corr);
160		maxcorr=find(list_corr==f);
 



161		strPlate=[strPlate letters(1,maxcorr)];
162	end	
163		
164	if	(i==3) || (i==4) || (i==5)
165		list_corr=[];
166		for j=1:10
167		corr=corr2(N(j).Image,char);
168		list_corr=[list_corr corr];
169		end
170		f=max(list_corr);
171		maxcorr=find(list_corr==f);
172		strPlate=[strPlate numbers(1,maxcorr)];
173	end	
174		
175	if	(i==2)
176		list_corr=[];
177		for j=1:26
178		corr=corr2(L(j).Image,char);
179		list_corr=[list_corr corr];
180		end
181		for j=1:10
182		corr=corr2(N(j).Image,char);
183		list_corr=[list_corr corr];
184		end
185		f=max(list_corr);
186		maxcorr=find(list_corr==f);
187		if maxcorr>26
188	strPlate=[strPlate numbers(1,maxcorr-26)];
189	else
190	strPlate=[strPlate letters1(1,maxcorr)];
191	end
192	end
193	
194	if (i==6)
195	list_corr=[];
196	for j=1:26
197	corr=corr2(L(j).Image,char);
198	list_corr=[list_corr corr];
199	end
200	for j=1:10
201	corr=corr2(N(j).Image,char);
202	list_corr=[list_corr corr];
203	end
204	f=max(list_corr);
205	maxcorr=find(list_corr==f);
206	if maxcorr>26
207	strPlate=[strPlate numbers(1,maxcorr-26)];
208	else
209	strPlate=[strPlate letters(1,maxcorr)];
210	end
211	end
212	end
213	end
 


214	%% If there aren't between 6 and 8 objects, the number plate is wrong %%
215	
216	if (Objects<6) || (Objects>8)
217	for i=1:8
218	strPlate{i}=0;
219	end
220	end
221	
222	end
