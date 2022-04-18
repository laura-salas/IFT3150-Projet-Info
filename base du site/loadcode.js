const CODE1URL = 'https://raw.githubusercontent.com/laura-salas/IFT3150-Projet-Info/main/assign_infos.py';
const CODE2URL = 'https://raw.githubusercontent.com/laura-salas/IFT3150-Projet-Info/main/embeddings_analysis.py';
function loadXMLDoc(theURL, varToLink)
    {
        if (window.XMLHttpRequest)
        {// code for IE7+, Firefox, Chrome, Opera, Safari, SeaMonkey
            xmlhttp=new XMLHttpRequest();
        }
        else
        {// code for IE6, IE5
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange=function()
        {
            if (xmlhttp.readyState==4 && xmlhttp.status==200)
            {
                // console.log(xmlhttp.responseText);
            }
        }
        xmlhttp.open("GET", theURL, false);
        xmlhttp.send();
    }
let assign_infos = "";
let embeddings_analysis = "";


// load code from repos and assign it to their vars 
var xmlhttp=false;
loadXMLDoc(CODE1URL);
if(xmlhttp==false){ /* set timeout or alert() */ }
else {assign_infos = xmlhttp.responseText;}
var xmlhttp=false;
loadXMLDoc(CODE2URL);
if(xmlhttp==false){ /* set timeout or alert() */ }
else {embeddings_analysis = xmlhttp.responseText;}

// apply the loaded code to the html elems 
var code1 = document.getElementById("code1");
var code2 = document.getElementById("code2");
code1.innerHTML = assign_infos;
code2.innerHTML = embeddings_analysis;

// syntax highlight
hljs.initHighlighting.called = false;
hljs.highlightAll();




