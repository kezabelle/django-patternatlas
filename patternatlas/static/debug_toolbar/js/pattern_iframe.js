;if (djdt !== void(0)) {

    // slightly older version of the debug_toolbar didn't namespace jQuery
    // so we'll try to bind the one in the global namespace.
    if (djdt.jQuery === void(0) && window.jQuery !== void(0)) {
        djdt.jQuery = window.jQuery;
    }

    (function ($) {
        $(document).on('click', '#djDebug .remoteIframe', function () {
            var self;
            var target;
            var location;
            var hash;
            var container;
            var url;

            self = $(this);
            target = self.attr('href').split('#');
            location = target[0];

            if (target.length === 1) {
                hash = '#p0'
            } else {
                hash = '#' + target[1];
            }
            container = $('.djdt-pattern-preview').eq(0);
            url = location + '?popup=1' + hash
            container.empty();
            container.html('<iframe src="' + url + '" seamless="seamless" sandbox="allow-same-origin" name="djdt-popup-iframe-pattern" frameborder="0" style="width: 100%; height: 100%;">');
            return false;
        });
    })(djdt.jQuery);
}
