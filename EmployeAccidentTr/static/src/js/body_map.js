odoo.define('EmployeAccidentTr.BodyWidget', function(require) {
    "use strict";

    const fieldRegistry = require('web.field_registry');
    const Field = require('web.AbstractField');

    const BodyWidget = Field.extend({
        template: false, // pas de QWeb, tout en JS
        start: function() {
            const self = this;
            const $container = $('<div style="position: relative; display:inline-block; width:100%; max-width:600px;"></div>');
            this.$el.append($container);

            const $img = $('<img src="/EmployeAccidentTr/static/img/body.png" style="width:100%; cursor:pointer;">');
            $container.append($img);

            // Afficher point existant
            if (self.value_x && self.value_y) {
                self._addMarker($container, self.value_x, self.value_y);
            }

            // Quand image cliquée
            $img.on('click', function(e) {
                const offset = $(this).offset();
                const x = e.pageX - offset.left;
                const y = e.pageY - offset.top;

                $container.find(".marker").remove();
                self._addMarker($container, x, y);

                self._setValue({x_click: x, y_click: y}); // sauvegarde champ
            });
        },

        _addMarker: function($container, x, y) {
            $('<div class="marker"></div>').css({
                position: 'absolute',
                top: (y-15) + 'px',
                left: (x-15) + 'px',
                width: '30px',
                height: '30px',
                background: 'red',
                borderRadius: '50%',
                border: '2px solid white',
                boxShadow: '0 0 8px black',
                zIndex: 1000,
            }).appendTo($container);
        },
    });

    fieldRegistry.add('body_widget', BodyWidget);
});
