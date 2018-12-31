<?php
    $conf=json_decode(file_get_contents("../config.json"));
    if(!$conf)die('No Config');
    
    $rss=simplexml_load_file($conf->rss[(int)$_GET['type']]->cache);
    for($i=0;$i<100;$i++){$listrss[$i]=getnews($rss,$i);}
    
    if($_GET['method']=='table') printtable($listrss);
    else if($_GET['method']=='show'){
        $page=$_GET['page']+1;
        echo preg_replace("/<a[^>]*>(.*?)<\/a>/is", "$1", $listrss[$page][1]);
        echo '<button onclick="back()" style="font-size:10px">返回</button>';
    }
    function printtable($list){
        $page=$_GET['page'];
        $id=0;
        for($i=10*$page+1;$i<=10*$page+10;$i++){
            echo '<tr><td onclick="select('.$id.');" id="'.$id.'">'.$list[$i][0].'</td></tr>';
            if($i>=99) break;
            $id++;
        }
    }
    function getnews($xml,$i){
        $title=@$xml->xpath("/rss/channel/item[".$i."]/title")[0];
        $content=@$xml->xpath("/rss/channel/item[".$i."]/description")[0];
        return array($title,$content);
    }
?>
