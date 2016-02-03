function checkEmpty() {
var valueofId=document.getElementById("id_email").value;
if (!valueofId) {
        alert('Search field is empty!');
        return false;
    }
}