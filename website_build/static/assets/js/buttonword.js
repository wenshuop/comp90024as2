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