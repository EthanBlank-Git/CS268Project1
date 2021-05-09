window.onload = function() {
    if( /Android|webOS|iPhone|iPad|Mac|Macintosh|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {  
        document.getElementById("header").style.height = "80px";
        document.getElementById("headerOverlay").style.height = "80px";
        document.getElementById("headerTitle").style.fontSize = "50px";
        document.getElementById("headerTitle").style.padding = "10px";
        document.getElementById("navBarButton").style.marginTop = "5px";
        document.getElementById("homeimgs").style.display =  "flex";
        document.getElementById("homeimgs").style.flexWrap =  "wrap";
    }
};



// Nav Bar
var isNavBarOpen = false;
function toggleNavBar() {
    // Variables
    var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    if (isNavBarOpen) {
        // Nav Bar
        document.getElementById("mainNavBar").style.width = "0px";
        // Nav Title
        document.getElementById("navTitle").style.marginLeft = "-200px";
        document.getElementById("navTitle").style.visibility = "hidden";
        // Nav Content
        document.getElementById("navContent").style.visibility = "hidden";
        // Nav Buttons
        document.getElementById("navBarButton").style.marginLeft = "5px";
        // Header
        document.getElementById("headerOverlay").style.marginLeft = "0px";
        document.getElementById("headerOverlay").style.width = "100%";
        // Main Content
        document.getElementById("main-div").style.marginLeft = "0";
        document.getElementById("main-div").style.width = "100%";

        // Handle Mobile displays
        if( /Android|webOS|iPhone|iPad|Mac|Macintosh|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {  
            document.getElementById("headerTitle").style.padding = "10px";
        }
        // Toggle variable
        isNavBarOpen = false;
    } else {
        var openedNavContentWidth = screenWidth - 275;
        // Nav Bar
        document.getElementById("mainNavBar").style.width = "275px";
        // Nav Title
        document.getElementById("navTitle").style.visibility = "visible";
        document.getElementById("navTitle").style.marginLeft = "0";
        // Nav Content
        document.getElementById("navContent").style.visibility = "visible";
        // Nav Button
        document.getElementById("navBarButton").style.marginLeft = "280px";
        // Header
        document.getElementById("headerOverlay").style.marginLeft = "275px";
        document.getElementById("headerOverlay").style.width = openedNavContentWidth + "px";
        // Main Content
        document.getElementById("main-div").style.marginLeft = "275px";
        document.getElementById("main-div").style.width = openedNavContentWidth + "px";

        

        // Handle Mobile displays
        if( /Android|webOS|iPhone|iPad|Mac|Macintosh|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {  
            document.getElementById("headerTitle").style.paddingLeft = "2000px";
        }

        // Toggle variable
        isNavBarOpen = true;
    }
}