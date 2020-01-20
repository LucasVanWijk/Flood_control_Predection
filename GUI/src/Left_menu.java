import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;

public class Left_menu {
    public static VBox create_left_menu() {
        //Left menu
        VBox vbox = new VBox();
        vbox.setPadding(new Insets(10));
        vbox.setSpacing(15);

        //Creates all the buttons
        Button button_ditch = Main.create_basic_button("Sloot",2);
        Button button_well = Main.create_basic_button("Put",1);

        //Adds all buttons to the left menu
        vbox.setAlignment(Pos.CENTER);
        vbox.getChildren().addAll(button_ditch,button_well);

        vbox.setBorder(new Border(new BorderStroke(Color.BLACK,
                BorderStrokeStyle.SOLID, CornerRadii.EMPTY, BorderWidths.DEFAULT)));

        return vbox;
    }
}
