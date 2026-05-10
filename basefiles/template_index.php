<?php
    require_once("AutoLoad.php");

    use App\Controller\DatabaseController;
    use App\Statics\Route;
    use App\Models\Project;

    session_start();

    $DatabaseController = new DatabaseController();

    Route::register_routes([
        "/" => "home",
        "/projects" => "projects",
        "/about", "about"
    ]);

    $int = 0;
    

    $request = Route::get_uri();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="./style/tailwind.css" rel="stylesheet">
    <title><?php $request ?></title>
</head>
<body class="bg-gray-700 text-white">
    <header>
        <?php
            Route::render_component("Navbar", [
                "pages" => ["home" => "", "projects" => "projects", "about" => "about"]
            ]);
        ?>
    </header>
    <main>
        <?php
            Route::render($request);
        ?>
    </main>
    <footer>

    </footer>
</body>
</html>
