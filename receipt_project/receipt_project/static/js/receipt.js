/* Project specific Javascript goes here. */

(function (win, $) {

    // sets date to current time
    var date;
    if (win.now) {
        // formatted based on django view variable
        date = moment(win.now, 'YYYY-MM-DDTHH-mm');
    } else {
        // now
        date = moment();
    }

    var update = function () {
        var url = '/events/' + date.format('YYYY-MM-DDTHH-mm');
        $.get(url, function (result) {
            $('body').html(result);
        });
    };

    var pressed_left = function () {
        // console.log('left');
        date.subtract('days', 1);
        update();
    };
    var pressed_right = function () {
        // console.log('right');
        date.add('days', 1);
        update();
    };
    var pressed_up = function () {
        // console.log('up');
        date.add('hours', 1);
        update();
    };
    var pressed_down = function () {
        // console.log('down');
        date.subtract('hours', 1);
        update();
    };

    // map key codes to functions
    var key_map = {
        37: pressed_left,
        39: pressed_right,
        38: pressed_up,
        40: pressed_down
    };

    // bind window to key event
    $(win).on('keydown', function (e) {
        var pressed = e.which;

        if (pressed in key_map) {
            e.preventDefault();
            key_map[pressed]();
        }
    });
    $(win).on('click', function (e) {
        win.print();
    });

    // initial load
    update();

})(window, $);