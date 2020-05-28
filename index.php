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
      <h3 class="card-title text-success">Armed</h3>
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
  <div class="card-header">Set Max Temperatures</div>
    <div class="card-body">
      <h5>
        Current set max furnace temp:</h5>
        <h3 class="text-warning">800 F </h3>
        <div class="input-group mb-3">
          <input type="text" class="form-control">
          <div class="input-group-append">
            <span class="input-group-text">F</span>
          </div>
        </div>
      <p class="card-text">
      <button type="button" class="btn btn-primary btn-md btn-block">Set</button>
      </p>
      <h5>
        Current set max house temp:
        </h5>
        <h3 class="text-primary">70 F</h3>
        <div class="input-group mb-3">
          <input type="text" class="form-control">
          <div class="input-group-append">
            <span class="input-group-text">F</span>
          </div>
        </div>
      <p class="card-text">
      <button type="button" class="btn btn-primary btn-md btn-block">Set</button>
      </p>
    </div>
  </div>

  
  
  
</div>
</div>


<!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  
</body>
</html>