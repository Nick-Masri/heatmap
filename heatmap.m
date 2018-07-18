% This is how you comment / document


% Calculates the color by feeding in the decimal 0-10
    % if decimal >=5
        % blue_value = ((10-decimal)/5)*255;
        % return (255 0 floor(blue_value));
    % else
        % red_value = (decimal/5)*255
        % return (floor(red_value) 0 255);
    % end

    
% 640 x 480 pixels
    
% A = [255, 255, 0]; % R
% A(:,:,2) = [0, 0, 0]; % G
% A(:, :, 3) = [0, 255, 255]; % B

%5 imshow(A)

stationstatelat = [
35.122879
35.121988
35.121407
35.084599
35.082406
35.081315000000004
35.086179
35.085782
35.086196
35.088336
35.082445
35.089774
35.086603000000004
35.086361
35.088003
35.051998
35.062534
35.055092
35.053832
35.052727000000004
35.054094
35.052146
35.054387
35.056761
35.040676
35.074219
35.082759
35.08603
35.083134
35.067786
35.057544
35.083197999999996
35.05081
35.075103999999996
35.078953000000006
35.08524
35.080303
35.074338
35.074675
35.078463
35.082415000000005
35.089073
35.132225
35.11607
35.123606
35.117971999999995
35.1244
35.05058
35.062665
35.071852
35.037549
35.055065
35.058256
35.072307
35.061174
35.109331
35.107996
35.099996000000004];

stationstatelong = [
137.138421
137.147907
137.137624
137.158981
137.160423
137.158806
137.158314
137.155079
137.15193
137.15852900000002
137.15703200000002
137.147987
137.156264
137.15563
137.155048
137.16706100000002
137.15925
137.15939699999998
137.158315
137.159269
137.154554
137.15606699999998
137.152995
137.175108
137.184311
137.12733
137.139185
137.13650900000002
137.13538799999998
137.140172
137.12944299999998
137.148168
137.136505
137.122273
137.149495
137.19030700000002
137.163341
137.17971
137.192045
137.18051100000002
137.16901299999998
137.188043
137.15994799999999
137.170769
137.178631
137.181456
137.170362
137.14004
137.142126
137.151837
137.138913
137.149279
137.1499
137.154785
137.145995
137.16633000000002
137.153393
137.163072];

stationids = [
2549
57
3
2014
9129
40
44
9132
9131
17
9
9130
100011
7
16
2015
43
55
49
22
66
38
9125
20
42
28
61
2010
47
46
2008
11
48
9118
10
51
13
60
1030
69
14
9128
2011
2016
59
58
2507
9121
67
65
1029
2013
37
19
70
68
64
45];

% find ranges of lat and long
rangelat = max(stationstatelat) - min(stationstatelat); % 0.0947 degrees (y)
rangelong = max(stationstatelong) - min(stationstatelong); % 0.0698 degrees (x)

% % size of each pixel in degrees for a 480 x 640 pixel map
% pixellat = rangelat/480; % 1.9724e-04
% pixellong = rangelong/640; % 1.0902e-04
% 
% % converts all lat and long to decimals with no whole numbers
% minus35lat = stationstatelat;
% minus137long = stationstatelong;
% 
% % calcs decimals spots for lat and long pixel locations
% pixelloclat = minus35lat*pixellat;
% pixelloclong = minus137long*pixellong;
% 
% scatter(pixelloclong, pixelloclat)

% get width and length
width = 640/rangelong;
length = 480/rangelat;

% get pixel locations
widthpixel = width * (stationstatelong - min(stationstatelong));
lengthpixel = length * (stationstatelat - min(stationstatelat));

% display scatter with station number labels
scatter(widthpixel, lengthpixel, 30, 'filled')

% stationid labels
labels = num2str((stationids),'%d');
text(widthpixel, lengthpixel, labels, 'horizontal', 'left', 'vertical', 'bottom')

% logical index labels
% labels = num2str((1:size(stationids,1))','%d');
% text(widthpixel, lengthpixel, labels, 'horizontal', 'left', 'vertical', 'bottom')