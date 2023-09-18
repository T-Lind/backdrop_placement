In this year's FTC game, I want to represent a backdrop, in which teams can put hexagonal tiles onto it, and stack them
vertically like honeycomb. The backdrop has a fixed width, and placing a hexagonal tile onto the stack earns them 5
points.

However, there are 4 different types of tiles, white, purple, green, and yellow. Most pixels are white, but there are
some of the other colors too. A mosaic can earn teams extra points, where if a cluster of 3 tiles (so all tiles are
touching the other two at the same time) of either the same color or ALL different colors earns a bonus of 10 points.
Finally, there's a height bonus for stacking the tiles - stacking 3 hexagonal tiles vertically earns 10 points (these
bonuses are only 1-time though), stacking 6 high earns another 10 points, and 9 high earns an additional 10 points.

So the question is, given this information, and the color of a tile our team currently has, how can we determine the
best location to drop off the hexagonal tile on the backdrop as a graph/tree problem?

The backdrop can fit 6 tiles on the first row, 7 tiles on the next, alternating 6/7 up to a maximum of 11 tiles high.