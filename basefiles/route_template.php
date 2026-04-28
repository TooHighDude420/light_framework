<?php
    namespace App\Statics;
    use ValueError;

    class Route
    {
        private static array $routes = [];

        public static function linkToAction(string $action)
        {
            return "php/$action.php";
        }

        public static function linkTo(string $location)
        {
            return "/$location";
        }

        public static function register_route(string $routename, string $viewname){
            if(isset(Route::$routes[$routename])){
                throw new ValueError("$routename already exists");
            } else {
                Route::$routes[$routename] = $viewname;
            }
        }

        public static function register_routes(array $routes){
            foreach ($routes as $key => $val){
                Route::register_route($key, $val);
            }
        }

        public static function get_uri(){
            if (isset(Route::$routes[$_SERVER['REQUEST_URI']])){
                $selector = Route::$routes[$_SERVER['REQUEST_URI']];
                return $selector;
            } else {
                throw new ValueError("Route not registerd or not found");
            }
        }

        public static function render(string $url): mixed {
            return include "App/View/$url.inc.php";
        }

        public static function render_component(string $name, $data){            
            extract($data);

            return include "App/View/Component/$name.comp.php";
        }
    }
