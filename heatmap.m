% This is how you comment / document


% Calculates the color by feeding in the decimal 0-10
    % if decimal >=5
        % blue_value = ((10-decimal)/5)*255;
        % return (255 0 floor(blue_value));
    % else
        % red_value = (decimal/5)*255
        % return (floor(red_value) 0 255);
    % end

x = [1, 2, 3];
y = [0, 1, 2];
c = [255, 0 ,0; 255, 0 ,255; 0, 0, 255];

scatter(x, y, 50, c, 'filled')