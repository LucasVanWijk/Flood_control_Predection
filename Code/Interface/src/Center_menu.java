import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;

import java.io.*;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Scanner;

public class Center_menu {
    static HBox create_center_menu() throws FileNotFoundException {
        HBox hbox = new HBox();

        VBox left_box = new VBox();
        VBox right_box = new VBox();
        Boolean file_exist = new File("Resultaten").exists();
        if (file_exist) {
            ArrayList<String> damages = read_and_return_damages();

            Label damage_old_situation = new Label(damages.get(0));
            Label damage_new_situation = new Label(damages.get(1));

            HBox left_text = new HBox(damage_old_situation);
            HBox right_text = new HBox(damage_new_situation);

            left_text.setAlignment(Pos.CENTER);
            right_text.setAlignment(Pos.CENTER);

            left_text.setBorder(new Border(new BorderStroke(Color.BLACK,
                    BorderStrokeStyle.SOLID, CornerRadii.EMPTY, BorderWidths.DEFAULT)));

            right_text.setBorder(new Border(new BorderStroke(Color.BLACK,
                    BorderStrokeStyle.SOLID, CornerRadii.EMPTY, BorderWidths.DEFAULT)));

            left_text.setPrefSize(250,250);
            right_text.setPrefSize(250,250);

            HBox left_pic = new HBox();
            HBox right_pic = new HBox();

            left_pic.setPrefSize(Integer.MAX_VALUE,Integer.MAX_VALUE-left_text.getHeight());
            right_pic.setPrefSize(Integer.MAX_VALUE,Integer.MAX_VALUE-right_text.getHeight());

            Image old_png = new Image("file:Resultaten/JPG_Test.JPG",1200,900,true,false);
            Image new_png = new Image("file:Resultaten/JPG_Test.JPG",1200,900,true,false);

            ImageView old_vieuw = new ImageView(old_png);
            ImageView new_vieuw = new ImageView(new_png);

//            left_pic.getChildren().add(old_vieuw);
//            right_pic.getChildren().add(new_vieuw);

//            old_vieuw.fitHeightProperty().bind(left_pic.heightProperty());
//            old_vieuw.fitWidthProperty().bind(left_pic.widthProperty());
//            new_vieuw.fitHeightProperty().bind(right_pic.heightProperty());
//            new_vieuw.fitWidthProperty().bind(right_pic.widthProperty());


            left_box.getChildren().addAll(old_vieuw,left_text);
            right_box.getChildren().addAll(new_vieuw,right_text);
        }

        left_box.setAlignment(Pos.BOTTOM_CENTER);
        right_box.setAlignment(Pos.BOTTOM_CENTER);

        left_box.setPrefWidth(Integer.MAX_VALUE);
        right_box.setPrefWidth(Integer.MAX_VALUE);

        left_box.setPrefHeight(Integer.MAX_VALUE);
        right_box.setPrefHeight(Integer.MAX_VALUE);

        left_box.setBorder(new Border(new BorderStroke(Color.BLACK,
                BorderStrokeStyle.SOLID, CornerRadii.EMPTY, BorderWidths.DEFAULT)));

        right_box.setBorder(new Border(new BorderStroke(Color.BLACK,
                BorderStrokeStyle.SOLID, CornerRadii.EMPTY, BorderWidths.DEFAULT)));

        hbox.getChildren().addAll(left_box, right_box);
        return hbox;
    }

    static ArrayList<String> read_and_return_damages() throws FileNotFoundException {
        ArrayList<String> damages = new ArrayList<String>();
        Scanner scanner = new Scanner(new File("Resultaten/text.csv"));
        scanner.useDelimiter(",");
        while(scanner.hasNext()){
            damages.add(scanner.next());
        }

        scanner.close();
        return damages;
    }
}
