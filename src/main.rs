extern crate wabt;
use wast::parser::{self, ParseBuffer};
use wast::Wat;
use std::fs;
use wabt::{Features, wasm2wat_with_features};
use std::fs::File;
use std::io::Read;
use std::env;


fn get_file_as_byte_vec(filename: &String) -> Vec<u8> {
    let mut f = File::open(&filename).expect("no file found");
    let metadata = fs::metadata(&filename).expect("unable to read metadata");
    let mut buffer = vec![0; metadata.len() as usize];
    f.read(&mut buffer).expect("buffer overflow");
    buffer
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut features = Features::new();
    features.enable_all();
    let wat:String = wasm2wat_with_features(get_file_as_byte_vec(&args[1]), features).unwrap();
    let buf = ParseBuffer::new(&wat[..]).unwrap();
    let _ast = parser::parse::<wast::Wat>(&buf).unwrap();
    fs::write("./parsed_debug.txt", format!("{_ast:#?}")).expect("Unable to write file");
}
