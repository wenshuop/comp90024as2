/* Team 13, Melbourne
Jing Qiu, 1152016, jiqiu1@student.unimelb.edu.au
Meijun Yue, 1190161, meijuny@student.unimelb.edu.au
Suyi Jiao, 1222833, sjjiao@student.unimelb.edu.au
Yeting Wu, 1310061, yetingw@student.unimelb.edu.au
Wenshuo Pan, 1226506, wenshuop@student.unimelb.edu.au */

var optionDate = $("#date").val();
var optionCity = $("#city").val();
if (!optionDate || !optionCity) {
    $("#word").attr('disabled', true);
}
const selectElement1 = document.querySelector('#date');
selectElement1.addEventListener('change', (event) => {
    var option_d = $("#date").val();
    var option_c = $("#city").val();
    if (!option_d || !option_c) {
        $("#word").attr('disabled', true);
    } else {
        $("#word").attr('disabled', false);
    }

});
const selectElement2 = document.querySelector('#city');
selectElement2.addEventListener('change', (event) => {
    var option_d = $("#date").val();
    var option_c = $("#city").val();
    if (!option_d || !option_c) {
        $("#word").attr('disabled', true);
    } else {
        $("#word").attr('disabled', false);
    }

});