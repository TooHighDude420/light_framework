<?php
    require_once("AutoLoad.php");

    use App\Controller\DatabaseController;
    use App\Statics\Route;

    session_start();

    $DatabaseController = new DatabaseController();

    Route::register_routes([
        "/" => "home",
        "/projects" => "projects",
        "/about", "about"
    ]);

    $request = Route::get_uri();
?>