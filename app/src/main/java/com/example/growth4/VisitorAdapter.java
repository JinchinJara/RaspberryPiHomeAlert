package com.example.growth4;

import android.content.Intent;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.firebase.ui.database.FirebaseRecyclerAdapter;
import com.firebase.ui.database.FirebaseRecyclerOptions;

public class VisitorAdapter extends FirebaseRecyclerAdapter<VisitorModel, VisitorAdapter.visitorsViewholder> {

    public VisitorAdapter (@NonNull FirebaseRecyclerOptions<VisitorModel> options) {
        super(options);
    }

    @Override
    protected void onBindViewHolder(@NonNull visitorsViewholder holder, int position, @NonNull VisitorModel model) {
        holder.name.setText(model.getName());
        holder.date.setText(model.getDate());
        holder.name2 = model.getName();
        holder.date2 = model.getDate();
        holder.path2 = model.getPath();
    }

    @NonNull
    @Override
    public visitorsViewholder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.visitor_item, parent, false);
        return new VisitorAdapter.visitorsViewholder(view);
    }

   class visitorsViewholder extends RecyclerView.ViewHolder{
        TextView name, date;
        String name2, date2, path2;
        public visitorsViewholder(@NonNull View itemView) {
            super(itemView);
            name = itemView.findViewById(R.id.name);
            date = itemView.findViewById(R.id.date);


            itemView.setOnClickListener (new View.OnClickListener(){
               @Override
               public void onClick(View v) {
                   int pos = getAdapterPosition();
                   if(pos != RecyclerView.NO_POSITION) {
                       Intent intent = new Intent(v.getContext(), VisitorImage.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                       intent.putExtra("name", name2);
                       intent.putExtra("date", date2);
                       intent.putExtra("path", path2);
                       v.getContext().startActivity(intent);
                       Log.d("Intent Transmitted", path2);
                   }
               }
            });

        }
    }
}
