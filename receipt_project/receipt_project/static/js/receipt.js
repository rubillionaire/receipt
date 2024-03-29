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

    // updates the fontend given the latest
    // state of the date object.
    var update = function () {
        var url = '/events/' + date.format('YYYY-MM-DDTHH-mm');
        $.get(url, function (result) {
            $('#receipt').html(result);
        });
    };

    // notifies server that a print
    // has a occured, so it can check
    // the queue
    var printed = function () {
        var url = '/printed/';
        $.get(url, function (status) {
            console.log(status);
        });
    };

    // functions that adjust the date
    // object's time based on which 
    // key is pressed
    var pressed = {
        left: function () {
            date.subtract('days', 1);
            update();
        },
        right: function () {
            date.add('days', 1);
            update();
        },
        up: function () {
            date.add('hours', 1);
            update();
        },
        down: function () {
            date.subtract('hours', 1);
            update();
        }
    };

    // map key codes to functions
    var key_map = {
        37: pressed.left,
        39: pressed.right,
        38: pressed.up,
        40: pressed.down
    };

    // watch for all key presses, in order
    // to adjust date object accordingly
    $(win).on('keydown', function (e) {
        var pressed = e.which;

        if (pressed in key_map) {
            e.preventDefault();
            key_map[pressed]();
        }
    });

    // map click to print function
    // notify server that a new print
    // has been added to the local queue
    $(win).on('click', function (e) {
        win.print();
        printed();
    });

    // update the page every minute
    var update_now = function () {
        date.add('minutes', 1);
        update();
    };
    win.setInterval(update_now, 60000);

    // grab the initial data set based
    // on the date object.
    update();

})(window, $);