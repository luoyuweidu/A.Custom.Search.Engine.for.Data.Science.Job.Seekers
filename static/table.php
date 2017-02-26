<!DOCTYPE html>
<html>


<title>W3.CSS</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/lib/w3.css">
<body>

<div class="w3-container">
<h2>Hoverable Table</h2>
<p>The w3-hoverable class adds a grey background color to all table rows when you mouse over them:</p>

<table class="w3-table w3-striped w3-bordered w3-border w3-hoverable">
<thead>
<tr class="w3-light-grey">
<th>Indeed Link</th>
<th>Score</th>
</tr>
</thead>

<tr>
<td>{{link1}}</td>
<td>{{score1}}</td>
</tr>
<tr>
<td>{{link2}}</td>
<td>{{score2}}</td>
</tr>
<tr>
<td>{{link3}}</td>
<td>{{score3}}</td>
</tr>



</table>
</div>

</body>


</html>
item list
item[0],item[1]




<?php
    for ($i=0, $i<3,$i++){
        echo
        '<tr>
        <td>{{link'.i.' }}</td>
        <td>{{score'.i.'}}</td>
            </tr>';
            
            
        }
            
            
    ?>

