window.onload=function(){
    //alert("page load!");

    chrome.runtime.sendMessage({command: "checkTab"});
}