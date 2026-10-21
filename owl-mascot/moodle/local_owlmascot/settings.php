<?php
// This file is part of Moodle - http://moodle.org/
defined('MOODLE_INTERNAL') || die();

if ($hassiteconfig) {
    $settings = new admin_settingpage('local_owlmascot', get_string('pluginname', 'local_owlmascot'));
    $ADMIN->add('localplugins', $settings);

    $settings->add(new admin_setting_configcheckbox('local_owlmascot/enabled',
        get_string('enabled', 'local_owlmascot'), get_string('enabled_desc', 'local_owlmascot'), 1));
    $settings->add(new admin_setting_configselect('local_owlmascot/corner',
        get_string('corner', 'local_owlmascot'), '', 'bottom-right', [
            'bottom-right' => get_string('bottom-right', 'local_owlmascot'),
            'bottom-left'  => get_string('bottom-left', 'local_owlmascot'),
        ]));
    $settings->add(new admin_setting_configtext('local_owlmascot/size',
        get_string('size', 'local_owlmascot'), get_string('size_desc', 'local_owlmascot'), 112, PARAM_INT));
    $settings->add(new admin_setting_configselect('local_owlmascot/shape',
        get_string('shape', 'local_owlmascot'), '', 'rounded', [
            'rounded' => get_string('shape_rounded', 'local_owlmascot'),
            'circle'  => get_string('shape_circle', 'local_owlmascot'),
            'square'  => get_string('shape_square', 'local_owlmascot'),
        ]));
    $settings->add(new admin_setting_configcheckbox('local_owlmascot/like',
        get_string('like', 'local_owlmascot'), get_string('like_desc', 'local_owlmascot'), 1));
    $settings->add(new admin_setting_configcheckbox('local_owlmascot/hideonquiz',
        get_string('hideonquiz', 'local_owlmascot'), get_string('hideonquiz_desc', 'local_owlmascot'), 1));
}
