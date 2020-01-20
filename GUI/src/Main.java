import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.*;
import javafx.scene.text.Font;
import javafx.stage.Modality;
import javafx.stage.Stage;

import java.io.FileNotFoundException;

public class Main extends Application {
    public static Stage window;
    public static BorderPane border;


    public static void main(String[] args) {
        launch(args);
    }


    public void start(Stage primaryStage) throws Exception {
        primaryStage.setMaximized(true);
        window = primaryStage;
        window.setTitle("James");

        //Adds all menu's together
        border = new BorderPane();
        border.setLeft(Left_menu.create_left_menu());
        border.setTop(Top_menu.create_top_menu());
        border.setCenter(Center_menu.create_center_menu());

        Scene s = new Scene(border);

        window.setScene(s);
        window.show();
    }


    public static Button create_basic_button(String name, int number_of_coordinates){
        Button x = new Button(name);
        x.setMinSize(180, 10);
        x.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                create_input_window(name,number_of_coordinates);
            }
        });

        return x;
    }


    public static void update_screen() throws FileNotFoundException {
        Main.border.setCenter(Center_menu.create_center_menu());
        Main.window.show();
    }


    private static void create_input_window(String title, int number_of_coordinates){
        Stage window = new Stage();

        //Block events to other windows
        window.initModality(Modality.APPLICATION_MODAL);
        window.setTitle(title);
        window.setMinWidth(window.getWidth()   + 300);
        window.setMinHeight(window.getHeight() + 300);

        VBox layout = new VBox(20);
        if (number_of_coordinates == 1){
            layout = create_standard_window_layout();
            HBox start_coordinate =  create_coordinate("Start coordinate: ");
            layout.getChildren().add(start_coordinate);
        }
        if(number_of_coordinates == 2){
            layout = create_standard_window_layout();
            HBox start_coordinate =  create_coordinate("Start coordinate: ");
            HBox end_coordinate =  create_coordinate("End coordinate: ");
            layout.getChildren().addAll(start_coordinate,end_coordinate);

        }

        Button closeButton = new Button("Close this window");
        closeButton.setOnAction(e -> window.close());
        closeButton.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                window.close();
                try {
                    run_simulation();
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
            }
        });

        layout.getChildren().add(closeButton);
        layout.setAlignment(Pos.CENTER);

        //Display window and wait for it to be closed before returning
        Scene scene = new Scene(layout);
        window.setScene(scene);
        window.showAndWait();

    }


    static void create_wait_window(){
        Stage window = new Stage();

        //Block events to other windows
        window.initModality(Modality.APPLICATION_MODAL);
        //window.setTitle(title);
        window.setMinWidth(window.getWidth()   + 300);
        window.setMinHeight(window.getHeight() + 300);

        Label wait_message =  new Label("De simulatie wordt uitgevoert even gedult AUB");
        Button closeButton = new Button("Close this window");
        closeButton.setOnAction(e -> window.close());

        VBox layout = new VBox(20);
        layout.getChildren().addAll(wait_message,closeButton);
        layout.setAlignment(Pos.CENTER);

        //Display window and wait for it to be closed before returning
        Scene scene = new Scene(layout);
        window.setScene(scene);
        window.showAndWait();

    }


    static HBox create_coordinate(String name){
        Font size = new Font(20);

        Label name_of_coordinate = new Label(name);

        HBox coordinate_hbox = new HBox();
        coordinate_hbox.setSpacing(20);
        Label x_coordinate_text = new Label("X: ");
        x_coordinate_text.setFont(size);
        TextField x_coordinate = new TextField();

        Label y_coordinate_text = new Label("Y: ");
        y_coordinate_text.setFont(size);
        TextField y_coordinate = new TextField();

        coordinate_hbox.getChildren().addAll(name_of_coordinate,x_coordinate_text,x_coordinate,y_coordinate_text,y_coordinate);

        return coordinate_hbox;
    }


    static VBox create_standard_window_layout(){
        Font size = new Font(20);

        VBox vBox = new VBox();
        vBox.setSpacing(20);

        Label window_text = new Label("vul hier in hoe diep de put zal zijn" +
                " en waar het zich zal verbinden") ;
        window_text.setFont(size);

        Label depth_text = new Label("Diepte: ");
        depth_text.setFont(size);
        TextField depth = new TextField();
        HBox depth_gui_line = new HBox();
        depth_gui_line.getChildren().addAll(depth_text,depth);
        vBox.getChildren().addAll(window_text,depth_gui_line);

        return vBox;
    }


    static void run_simulation() throws FileNotFoundException {

        create_wait_window();
        update_screen();

    }
}