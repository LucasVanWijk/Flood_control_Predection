import javafx.geometry.Pos;
import javafx.scene.layout.VBox;

public class Top_menu {
    public static VBox create_top_menu() {
        VBox top_menu = new VBox();
        top_menu.setAlignment(Pos.CENTER);

        top_menu.setSpacing(4);
        top_menu.setStyle("-fx-background-color: #336699;");

        return top_menu;
    }
}
