<!doctype html>
<html lang="en">
  <head>
    <style type="text/css">
    
        body { background: black !important; } /* Adding !important forces the browser to overwrite the default style applied by Bootstrap */
     </style>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

  </head>

<body>
<?php

$conn = new mysqli('localhost', "oliverpi", 'revilo', 'homeMonitoringStatus');
if ($conn->connect_error) {
  die("Error connecting to MySQL DB");
} 

$query = mysqli_query($conn, "SELECT TOP 1 FROM HouseSensors");
//$result = $query->fetch_all(MYSQLI_ASSOC);
//echo $result;
//print_r($result);

//$maxPlenumTemp= $result[0]['VariableValue'];
//$systemStatus = $result[1]['VariableValue'];
//$furnaceFanStatus = $result[2]['VariableValue'];
//$maxHouseTemp= $result[3]['VariableValue'];
//$airIntakeStatus = $result[4]['VariableValue'];



?>
<div class="mr-4 ml-4">
<div class="card-columns">
  <div class="card text-white bg-dark mb-3 mt-4">
  <div class="card-header">Current Time</div>
    <div class="card-body">
  
      <h3 class="card-title">
      <?php
          echo date("h:ia");
      ?> 
      </h3>
      <p class="card-text">
      <?php
        $mydate=getdate(date("U"));
        echo "$mydate[month] $mydate[mday], $mydate[year]";
      ?>
      </p>
    </div>
  </div>
  <div class="card text-white bg-dark mt-x mb-3">
  <div class="card-header">System Status</div>
  <div class="card-body">
      <h3 class="card-title text-success">
        <?php
        echo Armed
        ?>
      </h3>
      <p class="card-text">
      <button type="button" class="btn btn-danger btn-lg btn-block">Tap to unarm</button>
      </p>
    </div>
  </div>
  <div class="card text-white bg-dark mb-0 mt-x">
  <div class="card-header">Test System</div>
    <div class="card-body">
      <p class="card-text">
      <button type="button" class="btn btn-danger btn-lg btn-block">Activate Siren</button>
      </p>
    </div>
  </div>
  <div class="card text-white bg-dark mb-3 mt-4">
  <div class="card-header">Temperature Monitor</div>
  <div class="card-body">
      <h1 class="card-title text-warning">704.6 F</h1>
      <p class="card-text">Furnace Temperature</p>
      <h1 class="card-title text-primary">71.2 F</h1>
      <p class="card-text">House Temperature</p>

    </div>
  </div>
  <div class="card text-white bg-dark mb-3 mt-x">
  <div class="card-header">Air Intake Status</div>
    <div class="card-body">
      <h3 class="card-title">40% open</h3>
      <p class="card-text">
      <button type="button" class="btn btn-primary btn-lg btn-block">Close air intake</button>
      </p>
    </div>
  </div>
  
  <div class="card text-white bg-dark mt-4 mb-0 ">
  <div class="card-header">Furnace Fan Status</div>
    <div class="card-body">
      <h3 class="card-title text-success">On</h3>
      
    </div>
  </div>
  
  
  <div class="card text-white bg-dark mb-0 mt-3">
  <div class="card-header">House Status</div>
    <div class="card-body">
      <h5>
        Garage Door Status</h5>
        <h3 class="text-danger">Open</h3>
        
      <p class="card-text">
      </p>
      <h5>
        Front Door
        </h5>
        <h3 class="text-success">Closed and locked</h3>
        <div class="input-group mb-3">
        
    </div>
  </div>
</div>
</div>
</body>
</html>