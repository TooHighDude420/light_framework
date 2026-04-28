<?php
    spl_autoload_register(function ($class) {
        $baseDir = __DIR__ . '/';

        $file = $baseDir . str_replace('\\', '/', $class) . '.php';

        if (file_exists($file)) {
            require $file;
        } else {
            echo "Class file not found: $file\n";
        }
    });