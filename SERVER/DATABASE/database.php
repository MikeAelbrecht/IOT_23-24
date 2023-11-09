<?php
$servername = "localhost";
$username = "iot_lees";
$pass = "iot_lees";
$dbname = "iot";

function get_data()
{
    $conn = mysqli_connect($servername, $username, $pass, $dbname);

    if (!$conn)
    {
        die("Connection failed: " . mysqli_connect_error());
    }

    $sql = "SELECT datum, tijd FROM waarden";
    $result = mysqli_query($conn, $sql);

    if (mysqli_num_rows($result) > 0)
    {
        return $result;
    }
    
    return NULL;
}


?>