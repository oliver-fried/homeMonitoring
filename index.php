<!doctype html>
<!    Had to cd /dev  then chmod og+rwx gpio* then the Air Intake Status would work.>
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
$pythonScriptLocations = '/var/www/html/';

$systemStatus = "This feature is not functional yet";
$furnaceFanStatus = 'This feature is not functional yet';

if (shell_exec(escapeshellcmd('sudo python '.$pythonScriptLocations.'airIntakeStatus.py')) == 1) {
  $airIntakeStatus = "Open";
}

else if (shell_exec(escapeshellcmd('python '.$pythonScriptLocations.'airIntakeStatus.py'))==0) {
  $airIntakeStatus = "Closed";
}


$errors = exec('python '.$pythonScriptLocations.'airIntakeStatus.py 2>&1', $output);
echo $errors;
$houseTemp = shell_exec(escapeshellcmd('python '.$pythonScriptLocations.'houseTemp.py'));

$plenumTemp = shell_exec(escapeshellcmd('python '.$pythonScriptLocations.'plenumTemp.py'));

$garageStatus = "not working";
$frontDoorStatus = 'not working';




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

  <div class="card text-white bg-dark mb-0 mt-x">
  <div class="card-header">Temperature Monitor</div>
  <div class="card-body">
      <h1 class="card-title text-warning">
      <?php
        echo $plenumTemp;
        echo " F";
        ?>
      </h1>
      <p class="card-text">Furnace Temperature</p>
      <h1 class="card-title text-primary">
      <?php
        echo $houseTemp;
        echo " F";
        ?>
      </h1>
      <p class="card-text">House Temperature</p>

    </div>
  </div>

  <div class="card text-white bg-dark mb-3 mt-4">
  <div class="card-header">Air Intake Status</div>
    <div class="card-body">
      <h3 class="card-title"><?php echo $airIntakeStatus ?></h3>
      <p class="card-text">
      <form name="controlAirIntake" method="get" >
        <Button name = "controlAirIntake" type="submit" class="btn btn-primary btn-lg btn-block">Toggle Air Intake Position (Not functional)</Button>
      </form>
      <?php
      if (isset($_GET['controlAirIntake']))
      {
        shell_exec(escapeshellcmd('python3 '.$pythonScriptLocations.'airIntakeControl.py'));
      }
      ?>
      </p>
    </div>
  </div>

  <div class="card text-white bg-dark mt-x mb-3">
  <div class="card-header">System Status</div>
  <div class="card-body">
      <h3 class="card-title text-success">
        <?php
        echo $systemStatus;
        ?>
      </h3>
      <p class="card-text">
      <button type="button" class="btn btn-danger btn-lg btn-block">Tap to unarm</button>
      </p>
    </div>
  </div>

  <div class="card text-white bg-dark mb-0 mt-4">
  <div class="card-header">Test System</div>
    <div class="card-body">
      <p class="card-text">
      <form name="update" method="get" >
      <Button name = "update" type="submit" class="btn btn-primary btn-lg btn-block">(Not functional) Activate Alarm</Button>
      </form>
      <?php
      if (isset($_GET['update']))
      {
        shell_exec(escapeshellcmd('python3 '.$pythonScriptLocations.'activateAlarm.py'));
      }
      ?>
      </p>
    </div>
  </div>
  

  
  
  <div class="card text-white bg-dark mt-3 mb-0 ">
  <div class="card-header">Furnace Fan Status</div>
    <div class="card-body">
      <?php
        if ($furnaceFanStatus == 1) {
          echo "<h3 class=text-danger>"."Open"."</h3>";
        }

        else if ($furnaceFanStatus == 0) {
          echo "<h3 class=text-success>"."not functional yet"."</h3>";
        }

        else{
          echo "<h3 class=text-warning>"."Error reading garage Status"."</h3>";
        }
        ?>
      
    </div>
  </div>
  
  
  <div class="card text-white bg-dark mb-4 mt-3">
  <div class="card-header">House Status</div>
    <div class="card-body">
      <h5>
        Garage Door Status</h5>
        
        <?php
        if ($garageStatus == 1) {
          echo "<h3 class=text-danger>"."Open"."</h3>";
        }

        else if ($garageStatus == 0) {
          echo "<h3 class=text-success>"."Not functional yet"."</h3>";
        }

        else{
          echo "<h3 class=text-warning>"."Error reading garage Status"."</h3>";
        }
        ?>
        
      <p class="card-text">
      </p>
      <h5>
        Front Door
        </h5>
        <h3 class="text-success">
        <?php
        if ($frontDoorStatus == 1) {
          echo "<h3 class=text-danger>"."Unlocked"."</h3>";
        }

        else if ($frontDoorStatus == 0) {
          echo "<h3 class=text-success>"."not functional yet"."</h3>";
        }

        else{
          echo "<h3 class=text-warning>"."Error reading front door Status"."</h3>";
        }
        ?>

        </h3>
        <div class="input-group mb-3">
        
    </div>
  </div>
</div>
</div>

</body>
</html>
