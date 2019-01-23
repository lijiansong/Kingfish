// Create a div at the end of the document with the id "myfooter"

window.onload = function() {
    // Find the 'myfooter' element.
    var elem = document.getElementById('myfooter');
    if (!!elem) {
        elem.innerHTML = '<p><b>Team Members</b>: <i>Huang Hailong, Cao Lu, Li Jiansong</i></p>';
    }
    else {
        alert('WARN! Element "myfooter" not found!');
    }
};
