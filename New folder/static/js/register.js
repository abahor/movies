document.getElementById('my-form').onsubmit = function() {
    return isValidForm();
};
function isValidForm() {
      var i = document.getElementById('pass');
      var ir = document.getElementById('repass');
      var phone = document.getElementById('phone');
      if (i.value != ir.value || phone.value.length != 11){
        if(i.value != ir.value){
        document.getElementById("pass").style.border = "1px solid red";
        document.getElementById("repass").style.border = "1px solid red";
        alert('you should type the same password');
        return false;
      } else if ( phone.value.length != 11){
         phone.style.border = "1px solid red";
         alert('please enter a correct phone number');
         return false;
        }
        return false;
      }
      else {
        return true;
      }
}