<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <title>IOT control panel</title>
  </head>
  <body class="bg-secondary">
    <nav class="navbar navbar-expand-sm bg-secondary navbar-dark">
      <div class="container-fluid">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="./index.html">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" href="">Database</a>
          </li>
        </ul>
      </div>
    </nav>

    <div class="container-fluid p-5 bg-dark text-white text-center">
      <h1>IoT Control Panel</h1>
      <p>Here you can see all the timestamps when there was motion detected.</p>
    </div>

    <div class="container mt-3">
      <table class="table table-dark table-hover">
        <thead>
          <tr>
            <th>Date</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          <!-- for loop 
          <tr>
            <td>Date</td>
            <td>timestamp</td>
          </tr>
          -->
          <?php
          require_once("database.php");
          foreach (get_data() as $row)
          {
              echo "<tr>";
              echo "<td>" . $row["datum"] . "</td>";
              echo "<td>" . $row["tijd"] . "</td>";
              echo "</tr>";
          }
          ?>

        </tbody>
      </table>
    </div>
  </body>
</html>
