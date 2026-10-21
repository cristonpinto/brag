<?php
// This file is part of Moodle - http://moodle.org/

namespace local_owlmascot;

/**
 * Puts the owl on every normal page.
 */
class hook_callbacks {
    /** Layouts where a floating mascot would be wrong: pop-ups, print views, secure exams, maintenance. */
    private const SKIP_LAYOUTS = ['embedded', 'popup', 'print', 'frametop', 'redirect', 'maintenance', 'secure', 'login'];

    public static function before_footer_html_generation(\core\hook\output\before_footer_html_generation $hook): void {
        global $PAGE;

        if (!get_config('local_owlmascot', 'enabled') || !isloggedin() || isguestuser()) {
            return;
        }
        if (in_array($PAGE->pagelayout, self::SKIP_LAYOUTS, true)) {
            return;
        }
        // An animated mascot must never sit next to an assessed question.
        if (get_config('local_owlmascot', 'hideonquiz') && $PAGE->pagetype === 'mod-quiz-attempt') {
            return;
        }

        $config = [
            'corner' => get_config('local_owlmascot', 'corner') ?: 'bottom-right',
            'size'   => (int) (get_config('local_owlmascot', 'size') ?: 112),
            'shape'  => get_config('local_owlmascot', 'shape') ?: 'rounded',
            'like'   => (bool) get_config('local_owlmascot', 'like'),
            'moodle' => true,
            'label'  => get_string('arialabel', 'local_owlmascot'),
        ];

        $PAGE->requires->js(new \moodle_url('/local/owlmascot/owl-mascot.js'));
        $PAGE->requires->js_init_code('window.OwlMascot && window.OwlMascot.mount(' . json_encode($config) . ');');
    }
}
