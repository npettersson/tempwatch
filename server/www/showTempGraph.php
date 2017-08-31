<?php
$db_host = "localhost";
$db_name = "tempwatch";
$db_user = "tempwatch";
$db_pwd = "tempwatch";

try {
    $dbh = new PDO("mysql:host=$db_host;dbname=$db_name", $db_user, $db_pwd);

    /*** The SQL SELECT statement ***/
    $sth = $dbh->prepare("
        SELECT sensor_id, ROUND(AVG(temp_value),1) as temp_value, log_date
        FROM templog
        WHERE sensor_id in ('28-00000735dc64','28-00000735bce5')  
        AND log_date >= DATE_SUB(NOW(),INTERVAL 7 DAY)
        GROUP BY sensor_id, DATE(log_date), HOUR(log_date)
        ORDER BY log_date, sensor_id;
    ");
    $sth->execute();

    /* Fetch all of the remaining rows in the result set */
    $result = $sth->fetchAll(PDO::FETCH_ASSOC);

    /*** close the database connection ***/
    $dbh = null;
    
} catch(PDOException $e) {
    echo $e->getMessage();
}
$json_data = json_encode($result); 
?>

<!DOCTYPE html>
<meta charset="utf-8">
<style> /* set the CSS */

body { font: 12px Arial;}

path {
    stroke: steelblue;
    stroke-width: 2;
    fill: none;
}

.axis path,
.axis line {
    fill: none;
    stroke: grey;
    stroke-width: 1;
    shape-rendering: crispEdges;
}

.legend {
    font-size: 16px;
    font-weight: bold;
    text-anchor: middle;
}

</style>
<body>

<!-- load the d3.js library -->
<script src="http://d3js.org/d3.v3.min.js"></script>

<script>

// Set the dimensions of the canvas / graph
var margin = {top: 30, right: 20, bottom: 140, left: 50},
    width = 800 - margin.left - margin.right,
    height = 380 - margin.top - margin.bottom;

// Parse the date / time
var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

// Set the ranges
var x = d3.time.scale().range([0, width]);
var y = d3.scale.linear().range([height, 0]);

// Define the axes
var xAxis = d3.svg.axis().scale(x)
    .orient("bottom").ticks(10)
    .tickFormat(d3.time.format("%Y-%m-%d %H:%M"));

var yAxis = d3.svg.axis().scale(y)
    .orient("left").ticks(5);

// Define the line
var temperatureLine = d3.svg.line()
    .x(function(d) { return x(d.log_date); })
    .y(function(d) { return y(d.temp_value); });

// Adds the svg canvas
var svg = d3.select("body")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

// Get the data
<?php echo "data=".$json_data.";" ?>

data.forEach(function(d) {
    d.log_date = parseDate(d.log_date);
    d.temp_value = +d.temp_value;
});

// Scale the range of the data
x.domain(d3.extent(data, function(d) { return d.log_date; }));
y.domain([d3.min(data, function(d) { return d.temp_value; }), d3.max(data, function(d) { return d.temp_value; })]);

// Nest entries by sensor_id
var dataNest = d3.nest().key( function(d) { return d.sensor_id; } ).entries(data);
var color = d3.scale.category10();
legendSpace = width/dataNest.length

// Loop thru sensor_id and draw graph
dataNest.forEach(function(d,i) {
	svg.append("path")
		.attr("class", "line")
		.style("stroke", function() { return d.color = color(d.key); })
		.attr("id", 'tag' + d.key.replace(/\s+/g, ''))
		.attr("d", temperatureLine(d.values));
	
	svg.append("text")
		.attr("x", (legendSpace / 2) + i * legendSpace)
		.attr("y", height + (margin.bottom/2) + 5)
		.attr("class", "legend")
		.style("fill", function() { return d.color = color(d.key); } )
		.text( function() {
			if (d.key == '28-00000735dc64') { return "Innertemperatur"; }
			if (d.key == '28-00000735bce5') { return "Yttertemperatur"; }
			else { return d.key; } 
		});
});

// Add the X Axis
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .selectAll("text")  
    .style("text-anchor", "end")
    .attr("dx", "-.8em")
    .attr("dy", ".15em")
    .attr("transform", function(d) {
        return "rotate(-65)" 
    });

// Add the Y Axis
svg.append("g")
	.attr("class", "y axis")
	.call(yAxis);

</script>
</body>