<?php

namespace App\Statics;

use ValueError;

class Route
{
    private static array $routes = [];

    public static function linkToAction(string $action): string
    {
        return "php/$action.php";
    }

    public static function linkTo(string $location): string
    {
        return Route::get_route($location);
    }

    public static function register_route(string $routename, array | callable | string $viewname): void
    {
        if (isset(Route::$routes[$routename])) {
            throw new ValueError("$routename already exists");
        } else {
            Route::$routes[$routename] = $viewname;
        }
    }

    public static function register_routes(array $routes): void
    {
        foreach ($routes as $key => $val) {
            Route::register_route($key, $val);
        }
    }

    public static function get_uri(): mixed
    {
        if (isset(Route::$routes[$_SERVER['REQUEST_URI']])) {
            $selector = Route::$routes[$_SERVER['REQUEST_URI']];
            return $selector;
        } else {
            foreach (Route::$routes as $key => $val) {

                $pattern = preg_replace('/\{[^\/]+\}/', '([^/]+)', $key);
                $pattern = "#^" . $pattern . "$#";

                if (preg_match($pattern, $_SERVER['REQUEST_URI'], $matches)) {
                    array_shift($matches);

                    return [...$val, $matches[0]];
                }
            }

            throw new ValueError("Route not registerd or not found");
        }
    }

    public static function render(string | array $routename, $data = null): mixed
    {
        if ($data != null) {
            extract($data);
        }

        if (gettype($routename) == "array") {
            if (sizeof($routename) > 2) {
                $id = array_pop($routename);
                return $routename($id);
            } else {
                return $routename();
            }
        } else {
            return include "App/View/$routename.inc.php";
        }
    }

    public static function render_component(string $name, $data): mixed
    {
        extract($data);

        return include "App/View/Component/$name.comp.php";
    }

    public static function get_route(string $routename): mixed
    {
        $found = false;
        $route = "";

        foreach (Route::$routes as $key => $val) {
            if ($val == $routename && !$found) {
                $found = true;
                $route = $key;
                break;
            }
        }

        if ($found) {
            return $route;
        } else {
            throw new ValueError("Route not found");
        }
    }
}
