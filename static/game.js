let selfCount;
selfCount = 0;

function getCount(text){
    let newSelfCount = text.trim().split(/\s+/).length;
    if(newSelfCount != selfCount){
        selfCount = newSelfCount;
        updateBars();
    }
}

function updateBars() {
    $('#user-progress').val(selfCount);
}