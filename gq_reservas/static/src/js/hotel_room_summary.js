odoo.define("reservas.hotel_room_summary", function (require) {
    "use strict";

    var core = require("web.core");
    var registry = require("web.field_registry");
    var basicFields = require("web.basic_fields");
    var FieldText = basicFields.FieldText;
    var QWeb = core.qweb;
    var FormView = require("web.FormView");
    var py = window.py;

    var MyWidget = FieldText.extend({
        events: _.extend({}, FieldText.prototype.events, {
            change: "_onFieldChanged",
        }),
        init: function () {
            this._super.apply(this, arguments);
            if (this.mode === "edit") {
                this.tagName = "span";
            }
            this.set({
                date_to: false,
                date_from: false,
                summary_header: false,
                room_summary: false,
            });
            this.set({
                summary_header: py.eval(this.recordData.summary_header),
            });
            this.set({
                room_summary: py.eval(this.recordData.room_summary),
            });
        },
        start: function () {
            var self = this;
            if (self.setting) {
                return;
            }
            if (!this.get("summary_header") || !this.get("room_summary")) {
                return;
            }
            this.renderElement();
        },
        initialize_field: function () {
            FormView.ReinitializeWidgetMixin.initialize_field.call(this);
            var self = this;
            self.on("change:summary_header", self, self.start);
            self.on("change:room_summary", self, self.start);
        },
        renderElement: function () {
            this._super();
            this.$el.html(
                QWeb.render("RoomSummary", {
                    widget: this,
                })
            );
        },
        _onFieldChanged: function (event) {
            this._super();
            this.lastChangeEvent = event;
            this.set({
                summary_header: py.eval(this.recordData.summary_header),
            });
            this.set({
                room_summary: py.eval(this.recordData.room_summary),
            });
            this.renderElement();
        },
    });

    registry.add("Room_Reservation", MyWidget);
    return MyWidget;
});
