var spotCount = 1

function addOneMoreSpot(plusElement)
{
    spotCount++;
    $(plusElement).before(
        `<div class="form-group">
            <label for="spot${spotCount}">Spot${spotCount}:</label>
            <input type="text" class="form-control" id="spot${spotCount}" name="spot${spotCount}" placeholder="Coordinates">
            <button class="btn btn-default btn-sm" type="button" onclick="addOneMoreSpot(this)">+</button>
        </div>`
    );
    plusElement.remove();
}

function readURL(input)
{
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#pimg').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$("#file").change(function(){
    readURL(this);
    $("#pimg").removeAttr('hidden');
});
