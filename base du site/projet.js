let wordFound = true;

document.querySelector('#word').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      searchWord();
    }
});

function getPairInfo(word){
    var pairInfo = null;
    for(var i = 0; i < data.length; i++){
        if (data[i]["paire (f)"].trim() === word.trim() || data[i]["paire (m)"].trim() === word.trim()) pairInfo = data[i];
    }

    return pairInfo;
    
}

function setElemText(id, text){
    document.getElementById(id).innerText = text;
}

function toggleAlert(word){
    let alerty = document.getElementById("alerty");
    if (wordFound){
        alerty.innerHTML = "";
    }
    else {
        alerty.innerHTML = `
        <div  class="alert alert-danger alert-dismissible fade show" role="alert">
        Word "` + word + `" not found in database!
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
        `;
    }
}
function loadInfoForWord(word){
    if (word == "") return;
    let pairInfo = getPairInfo(word);
    if (pairInfo != null){
        wordFound = true;
        toggleAlert(word);
        var word_id = pairInfo["global_ref"];
        var word_m = pairInfo["paire (m)"];
        var word_f = pairInfo["paire (f)"];
        var freq_f = pairInfo["frequence_f"];
        var freq_m = pairInfo["frequence_m"];
        var simScore = pairInfo["similarite"];
        var stemmedScore = pairInfo["stemmed_score"];
        var lemmaScore = pairInfo["lemma_score"];
        var pureScore = pairInfo["pure_score"];
        var neighbours_f = pairInfo["voisins_f"];
        var neighbours_m = pairInfo["voisins_m"];
        var freq_neighbours_f = pairInfo["neighbours_frequences_f"];
        var freq_neighbours_m = pairInfo["neighbours_frequences_m"];
        
        setElemText("global_ref", word_id);
        setElemText("paire (f)", word_f);
        setElemText("paire (m)", word_m);
        setElemText("frequence_f", freq_f);
        setElemText("frequence_m", freq_m);
        setElemText("similarite", simScore.toFixed(3));
        setElemText("pure_score", pureScore);
        setElemText("lemma_score", lemmaScore);
        setElemText("stemmed_score", stemmedScore);
        
        for(var i = 0; i < neighbours_f.length; i++){
            getElemFromIdAndIdx("f-neighbours", 0).innerText = 'Neighbours of "' + word_f + '"';
            setNewNeighbour("f-neighbours", i+1, neighbours_f[i], freq_neighbours_f[i]);
            getElemFromIdAndIdx("m-neighbours", 0).innerText = 'Neighbours of "' + word_m + '"';
            setNewNeighbour("m-neighbours", i+1, neighbours_m[i], freq_neighbours_m[i]);

        }
    }
    else {
        wordFound = false;
        toggleAlert(word);
    }
}


function searchWord(){
    var wordToSearch = document.getElementById("word").value.trim();
    loadInfoForWord(wordToSearch);
    // alert(wordToSearch);
}

// to get child: .children[0]
function getElemFromIdAndIdx(id, idx){
    return document.getElementById(id).children[idx];
}

function loadWordList(){
    let wordlist = document.getElementById('wordlist');
    for (var i = 0; i < data.length; i++){
        word_m = data[i]["paire (m)"];
        word_f = data[i]["paire (f)"];
        var wordElem = `
    <button type="button" class="list-group-item list-group-item-action" onclick="loadInfoForWord('` + word_m +`')">`+ word_m + " | " + word_f + `</button>`;
        wordlist.innerHTML += wordElem;
    }
    // var wordElem = `
    // <button type="button" class="list-group-item list-group-item-action" onclick="loadInfoForWord('` + word_m `')">`+ word_m + "|" + word_f +`</button>`;
}


function setNewNeighbour(id, idx, newNeighbour, nbOccurrences){
    var newWord = newNeighbour.split("_")[0]; // remove POS 
    getElemFromIdAndIdx(id, idx).innerHTML = newWord + " (" +
    newNeighbour.split("_")[1] + ")"  
      + 
    `
    ` + '<span class="badge bg-secondary rounded-pill">' + nbOccurrences + " occurrences" + '</span>';
}

function searchWordByNeighbourIdx(id, idx){
    var clickedWord = getElemFromIdAndIdx(id, idx).innerText.split("\n")[0].split("(")[0].trim();
    console.log(clickedWord);
    loadInfoForWord(clickedWord);
}

window.onload = function() {
    loadWordList();
}